from typing import Iterable, List

import pandas as pd
from sklearn.cluster import AgglomerativeClustering, KMeans


def read_results(path='data/abstimmungen.csv') -> pd.DataFrame:
    """
    Reads results form filesystem and returns dataframe. Also cleans some of the code.
    """
    results = pd.read_csv(path, na_values=["..."])
    results.rename(
        columns={"Kanton (-) / Bezirk (>>) / Gemeinde (......)": "Gemeinde"},
        inplace=True)
    results["Gemeinde"] = results["Gemeinde"].str.replace(".", "")
    results[["Datum",
             "Vorlage"]] = results["Datum und Vorlage"].str.split(" ",
                                                                  1,
                                                                  expand=True)
    results["Datum"] = results["Datum"].astype('datetime64')

    return results


def get_pivot(data_frame: pd.DataFrame, values: Iterable[str]) -> pd.DataFrame:
    """
    Brings the methods into a format that we can use to run clustering algorithms
    """
    pivot = data_frame.pivot(index="Gemeinde",
                             columns="Datum und Vorlage",
                             values=values).reset_index()
    pivot.columns.name = None
    pivot.fillna(pivot.mean(), inplace=True)

    return pivot


def get_votations(data_frame: pd.DataFrame) -> List[str]:
    """Retuns a list of the voations in the given dataframe"""
    return data_frame["Datum und Vorlage"].unique()


def cluster_pivot_kmeans(pivot: pd.DataFrame,
                         votations: Iterable[str]) -> pd.DataFrame:
    """
    Run the k-means algorithm to cluster the pivot with the given votations columns
    """
    results = pivot.copy()

    for k in range(2, 15, 1):
        k_means = KMeans(n_clusters=k)
        k_means.fit(pivot.filter(votations, axis=1))
        results[f'Cluster (k={k})'] = k_means.labels_

    return results


def cluster_pivot_agglomerative(pivot: pd.DataFrame,
                                votations: Iterable[str]) -> pd.DataFrame:
    """
    Run the agglomerate clustering algorithm to cluster the pivot with the given columns
    """
    results = pivot.copy()

    for k in range(2, 15, 1):
        ag = AgglomerativeClustering(n_clusters=k)
        ag.fit(pivot.filter(votations, axis=1))
        results[f"Cluster (k={k})"] = ag.labels_

    return results


class Manager:
    """
    This class manages the different dataframes that we use in our datastory.

    It loads the files from the filesystem and stores the results of the algorithms
    """
    results: pd.DataFrame = None    # Original results data
    yes_pivot: pd.DataFrame = None    # Table with communes and votes
    votations: List[str] = None    # List of all votes in the data

    k_means_results: pd.DataFrame = None    # Store results from clustering
    agglomerative_results: pd.DataFrame = None
    votation_clusters: pd.DataFrame = None

    portrait: pd.DataFrame = None    # Store stats about communes
    joined_data: pd.DataFrame = None    # Combination of clustered communes with stats

    def __init__(self, path):
        self.path = path

    def load_results(self):
        """
        Loads the result from the database and converts them into the formats that we use later,
        this has to run before any clustering can happen.
        """
        self.results = read_results(self.path)
        self.yes_pivot = get_pivot(self.results, "Ja in %")
        self.votations = get_votations(self.results)

    def cluster_results_kmeans(self, selected):
        """
        Run the kmeans on the selected votations and store results in manager
        """
        self.k_means_results = cluster_pivot_kmeans(self.yes_pivot, selected)

    def cluster_results_agglomerative(self, selected):
        """
        Run agglomerative cluster and store results in manager
        """
        self.agglomerative_results = cluster_pivot_agglomerative(
            self.yes_pivot, selected)

    def cluster_results_grouped(self, k, n):
        """
        Run agglomerative cluster based on groupd votations and store results in manager,
        You have to run `cluster_votations` first.
        """
        selected = self.votation_clusters[self.votation_clusters[
            f"C{k}" == n]]["Datum und Vorlage"]
        self.cluster_results_agglomerative(selected)
        self.cluster_results_kmeans(selected)

    def cluster_votations(self):
        """
        Run agglomerative cluster on votations and store results
        """
        votation_pivot = self.results.pivot(index="Datum und Vorlage",
                                            columns="Gemeinde",
                                            values="Ja in %").reset_index()
        votation_pivot.fillna(0, inplace=True)
        votation_pivot.columns.name = None
        votation_clusters = pd.DataFrame(
            votation_pivot["Datum und Vorlage"].copy())
        for k in range(2, 30, 1):
            ag = AgglomerativeClustering(n_clusters=k)
            ag.fit(votation_pivot.drop(["Datum und Vorlage"], axis=1))
            votation_clusters[f"C{k}"] = ag.labels_

        self.votation_clusters = votation_clusters

    def cluster_votation_group(self, k, n) -> List[str]:
        """
        Returns a list of the votations that are in the cluster `k` if clustered in `n` groups.
        """
        return self.votation_clusters[self.votation_clusters[f"C{k}"] ==
                                      n]["Datum und Vorlage"]

    def export(self, filename: str):
        """
        Save the generated dataframes to an excel sheet.
        """
        summaries = [
            self.cluster_results_agglomerative.groupby(
                f'Cluster (k={i})').describe(include=[float])
            for i in range(2, 15)
        ]
        summaries = pd.concat(summaries,
                              keys=range(2, 15),
                              names=["Nr. of Clusters", "n"])
        with pd.ExcelWriter(filename) as writer:
            summaries.to_excel(writer, sheet_name="Zusammenfassung")
            self.joined_data.to_excel(writer, sheet_name="Gemeinden")

    def read_portrait(self, path="data/gemeindeportrait.xlsx"):
        """
        Load the statistics into the manager and clean them a bit
        """
        portrait = pd.read_excel(
            'data/gemeindeportrait.xlsx', ).rename(columns={
                'Gemeindename': 'Gemeinde'
            }).set_index('Gemeinde')

        for col in portrait.columns:
            portrait[col] = pd.to_numeric(portrait[col], errors='coerce')
        self.portrait = portrait.dropna(subset=["Gemeindecode"])

    def join_portrait(self):
        """
        Combines the clustered data with the statistics about the communes
        """
        self.joined_data = self.agglomerative_results.join(self.portrait,
                                                           on="Gemeinde")

    def get_cluster(self, k, n) -> pd.DataFrame:
        """
        Return a extract from the data frame in the selected cluster
        """
        return self.joined_data[self.joined_data[f'Cluster (k={k})'] == n]
