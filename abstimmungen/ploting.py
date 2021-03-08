"""
Methods for presenting plots. Most of them are not used in the final notebook.
They are used in the Notebook that was used to explore the data.
"""
from typing import List
import ipywidgets as widgets
import matplotlib
from IPython.display import HTML, SVG, display
from ipywidgets import interact, interact_manual
from lxml import etree
from matplotlib import pyplot as plt


def votation_select_widget(votations):
    return widgets.SelectMultiple(
        options=votations,
        value=tuple(votations[:6]),
        rows=10,
        layout=widgets.Layout(width="80%"),
    )


def single_select_widget(votations, description, index=0) -> widgets.Dropdown:
    return widgets.Dropdown(options=votations,
                            value=votations[index],
                            description=description)


def print_group(k, n, votation_clusters):
    names = votation_clusters[votation_clusters[f"C{k}"] ==
                              n]["Datum und Vorlage"]

    display(HTML(f"<h3>Cluster {n} of {k}</h3>"))
    for name in names:
        print(name)
    if len(names) == 0:
        print()


def plot_results(x, y, k, ag_results, kMeans_results):
    if kMeans_results is not None:
        f, (ax1, ax2) = plt.subplots(1, 2, sharex=True, sharey=True)

        scatter1 = ax1.scatter(ag_results[x],
                               ag_results[y],
                               c=ag_results[f'Cluster (k={k})'],
                               s=8,
                               cmap="tab20")
        ax1.grid()
        ax1.set_title("Agglomerative")
        ax1.set_ylabel(y, wrap=True)
        ax1.set_xlabel(x, wrap=True)
        handles1, labels1 = scatter1.legend_elements(prop="colors")
        ax1.legend(handles1, labels1, loc="upper left", title="Cluster")

        scatter2 = ax2.scatter(kMeans_results[x],
                               kMeans_results[y],
                               c=kMeans_results[f'Cluster (k={k})'],
                               s=8,
                               cmap="tab20")
        ax2.grid()
        ax2.set_title("K-Means")
        ax2.set_xlabel(x)
        handles2, labels2 = scatter2.legend_elements(prop="colors")
        ax2.legend(handles2, labels2, loc="upper left", title="Cluster")
        f.tight_layout()
    else:
        f, ax1 = plt.subplots(1, 1, sharex=True, sharey=True)

        scatter1 = ax1.scatter(ag_results[x],
                               ag_results[y],
                               c=ag_results[f'Cluster (k={k})'],
                               s=8,
                               cmap="tab20")
        ax1.grid()
        ax1.set_title("Agglomerative")
        ax1.set_ylabel(y, wrap=True)
        ax1.set_xlabel(x, wrap=True)
        handles1, labels1 = scatter1.legend_elements(prop="colors")
        ax1.legend(handles1, labels1, loc="upper left", title="Cluster")
        f.tight_layout()


def show_stats_for(pivot, votation):
    if votation:
        ax = pivot.boxplot(
            column=[v for v in votation],
            fontsize=8,
            rot=40,
            sym="g+",
        )
        ax.set_ylabel("Zustimmung in %")
        plt.title("Boxplot der Abstimmungen")


def show_portrait_table(data, k, col):
    display(data.groupby(f'Cluster (k={k})')[col].describe())


def show_portrait_boxplot(data, k, col):
    data.boxplot(column=col,
                 by=f'Cluster (k={k})',
                 meanline=True,
                 showmeans=True,
                 showfliers=False)


def plot_portrait_clusters(x, y, k, title="Test", results=None):
    if results is None:
        print("Generate clusters first!")
        return
    scatter = plt.scatter(results[x],
                          results[y],
                          c=results[f'Cluster (k={k})'],
                          s=8,
                          cmap="tab20")
    plt.grid()
    plt.title(title)
    plt.ylabel(y, wrap=True)
    plt.xlabel(x, wrap=True)
    handles, labels = scatter.legend_elements(prop="colors")
    plt.legend(handles, labels, loc="upper left", title="Cluster")


def get_colorstring(color) -> str:
    """Turn a rgb color into a hex color"""
    return f"#{int(color[0]*255):02x}{int(color[1]*255):02x}{int(color[2]*255):02x}"


def show_map(data, k):
    svg = etree.parse('data/swiss.svg').getroot()
    cmap = matplotlib.cm.get_cmap('tab20')
    for e in svg.findall(".//{http://www.w3.org/2000/svg}path"):
        geo_id = e.get('id')
        g = int(geo_id.split('_')[-1])
        f = data["Gemeindecode"] == g

        if f.any():
            n = data[data["Gemeindecode"] == g][f"Cluster (k={k})"].values[0]
            color = get_colorstring(cmap(n))
            e.set('fill', color)
    display(HTML(f"<h3>K={k}</h3>"))
    display(SVG(etree.tostring(svg)))


def explore_stats(manager, selected, stat, ref, k, sparse=True):
    manager.cluster_results_agglomerative(selected)
    manager.join_portrait()
    if not sparse:
        fig, axes = plt.subplots(nrows=int(k / 3),
                                 ncols=3,
                                 sharex=True,
                                 sharey=True)

        manager.joined_data.hist(column=stat,
                                 by=f"Cluster (k={k})",
                                 figsize=(15, 10),
                                 bins=20,
                                 histtype="step",
                                 ax=axes)
        fig.text(0.5, 0.04, stat)
        fig.text(0.04, 0.5, "Verteilung", va="center", rotation="vertical")

        fig.suptitle(f"{stat} pro Gruppe")
        plt.show()

        scatter = plt.scatter(
            x=manager.joined_data[stat],
            y=manager.joined_data[ref],
            c=manager.joined_data[f"Cluster (k={k})"],
            cmap="tab20",
        )
        plt.grid()
        plt.title(stat)
        plt.xlabel(stat, wrap=True)
        plt.ylabel(ref, wrap=True)
        handles, labels = scatter.legend_elements(prop="colors")
        plt.legend(handles, labels, title="Cluster")
        plt.show()

    desc = manager.joined_data.groupby(f"Cluster (k={k})")[[
        stat, ref
    ]].describe().sort_values((stat, "50%"))

    display(desc)
    desc = desc.reset_index()

    moments = [('max', '^'), ('75%', '2'), ('50%', 'o'), ('mean', 'x'),
               ('25%', '1'), ('min', 'v')]

    scatter = None

    for moment, marker in moments:

        scatter = plt.scatter(desc[(stat, '50%')],
                              desc[(ref, moment)],
                              c=desc[f"Cluster (k={k})"],
                              cmap="tab20",
                              marker=marker,
                              label=moment)

    handles, labels = scatter.legend_elements(prop="colors")

    color_legend = plt.legend(handles,
                              labels,
                              title="Cluster",
                              loc="best",
                              bbox_to_anchor=(0.5, 0., 0.5, 1.0))

    plt.grid()
    plt.title("Deskriptive Werte der Cluster")
    plt.xlabel(stat + " [Cluster-median]", wrap=True)
    plt.ylabel(ref, wrap=True)

    plt.legend(loc="best", bbox_to_anchor=(0.0, 0., 0.5, 1.0))
    plt.gca().add_artist(color_legend)
    plt.show()


def show_single_map(data, k, n):
    svg = etree.parse('data/swiss.svg').getroot()
    for e in svg.findall(".//{http://www.w3.org/2000/svg}path"):
        geo_id = e.get('id')
        g = int(geo_id.split('_')[-1])
        f = (data["Gemeindecode"] == g) & (data[f'Cluster (k={k})'] == n)

        if f.any():
            e.set('fill', "#ff00ff")

    display(HTML(f"<h2>K={k}, N={n}</h2>"))
    display(SVG(etree.tostring(svg)))


class Viewer:
    """
    Has a Manager with data and can draw plots from it
    """
    def __init__(self, data):
        self.data = data
        self.votation_select = votation_select_widget(self.data.votations)

    def explore_yes_pivot(self):
        """
        Show a widget to explore the votation data
        """
        interact(self.explore, votation=self.votation_select)

    def print_group(self, k, n):
        """
        Show selected votation group
        """
        self.votation_k = k
        self.votation_n = n
        print_group(k, n, self.data.votation_clusters)

    def scatter_explorer(self, all_votations=False):
        """
        Explore the clusters
        """
        if all_votations:
            selected_votations = self.data.votations
        else:
            selected_votations = self.get_selected_votations()
        x = widgets.Dropdown(options=selected_votations,
                             value=selected_votations[0],
                             description="X")
        y = widgets.Dropdown(options=selected_votations,
                             value=selected_votations[1],
                             description="Y")
        k = k = widgets.IntSlider(min=2,
                                  max=14,
                                  readout=True,
                                  description="Clusters")
        ui = widgets.HBox([x, y, k])
        out = widgets.interactive_output(self.plot_clusters_scatter, {
            'x': x,
            'y': y,
            'k': k
        })

        display(ui, out)

    def scatter_explorer_single(self, all_votations=False):
        if all_votations:
            selected_votations = self.data.votations
        else:
            selected_votations = self.get_selected_votations()

        x = widgets.Dropdown(options=selected_votations,
                             value=selected_votations[0],
                             description="X")
        y = widgets.Dropdown(options=selected_votations,
                             value=selected_votations[1],
                             description="Y")
        k = k = widgets.IntSlider(min=2,
                                  max=14,
                                  readout=True,
                                  description="Clusters")
        ui = widgets.HBox([x, y, k])
        out = widgets.interactive_output(self.plot_clusters_scatter_single, {
            'x': x,
            'y': y,
            'k': k
        })

        display(ui, out)

    def plot_clusters_scatter(self, x, y, k):
        if hasattr(self.data, "k_means_results"):
            plot_results(x, y, k, self.data.agglomerative_results,
                         self.data.k_means_results)
        else:
            self.plot_clusters_scatter_single(x, y, k)

    def plot_clusters_scatter_single(self, x, y, k):
        plot_results(x, y, k, self.data.agglomerative_results, None)

    def print_groups(self, k, n):
        print_group(k, n, self.data.votation_clusters)

    def show_table(self, k, col):
        display(
            self.data.joined_data.groupby(f'Cluster (k={k})')[col].describe())

    def show_boxplot(self, k, col):
        self.data.joined_data.boxplot(column=col,
                                      by=f'Cluster (k={k})',
                                      meanline=True,
                                      showmeans=True,
                                      showfliers=False)

    def plot_portrait_clusters(self, x, y, k, title="Title"):
        plot_portrait_clusters(x, y, k, title, self.joined_data)

    def explore(self, votation):
        show_stats_for(self.data.yes_pivot, votation)

    def get_selected_votations(self) -> List[str]:
        return self.votation_select.value

    def get_selected_votation_group(self) -> List[str]:
        return self.data.cluster_votation_group(self.votation_k,
                                                self.votation_n)

    def show_portrait_table(self, k, col):
        show_portrait_table(self.data.joined_data, k, col)

    def show_portrait_boxplot(self, k, col):
        show_portrait_boxplot(self.data.joined_data, k, col)

    def explore_single_portrait(self):
        k_slider = widgets.IntSlider(min=2, max=14)
        cols = widgets.Dropdown(
            options=list(self.data.joined_data.columns.drop(["Gemeinde"])))
        input_ui = widgets.HBox([k_slider, cols])

        table_out = widgets.interactive_output(self.show_portrait_table, {
            'k': k_slider,
            'col': cols
        })
        boxplot_out = widgets.interactive_output(self.show_portrait_boxplot, {
            'k': k_slider,
            'col': cols
        })
        tab_headers = ["table", "boxplot"]

        tab_children = [
            table_out,
            boxplot_out,
        ]

        tabbed_view = widgets.Tab()
        tabbed_view.children = tab_children

        for i, title in enumerate(tab_headers):
            tabbed_view.set_title(i, title)

        return display(input_ui, tabbed_view)

    def plot_portrait_clusters(self, x, y, k, title):
        plot_portrait_clusters(x, y, k, title, self.data.joined_data)

    def scatter_portrait(self):
        x = widgets.Dropdown(
            options=list(self.data.joined_data.columns.drop(['Gemeinde'])))
        y = widgets.Dropdown(
            options=list(self.data.joined_data.columns.drop(['Gemeinde'])))
        k = widgets.IntSlider(min=2, max=15)
        title_widget = widgets.Text()

        input_ui = widgets.HBox([x, y, k, title_widget])

        plot_out = widgets.interactive_output(self.plot_portrait_clusters, {
            'x': x,
            'y': y,
            'k': k,
            'title': title_widget
        })

        display(input_ui, plot_out)

    def show_map(self):
        k = widgets.IntSlider(min=2, max=14, continues_update=False)

        interact_manual(lambda k: show_map(self.data.joined_data, k), k=k)

    def show_single_cluster_map(self):
        k = widgets.IntSlider(min=2, max=14, continues_update=False)
        n = widgets.IntSlider(min=0, max=13, continues_update=False)

        interact_manual(
            lambda k, n: show_single_map(self.data.joined_data, k, n),
            k=k,
            n=n)
