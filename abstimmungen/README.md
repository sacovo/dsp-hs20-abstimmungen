# Resultate von SVP-typischen Abstimmungsvorlagen im Verlaufe der Zeit
Team: Sandro Covo

## Goals:

Die Abstimmungsresultate von SVP-Typischen Abstimmungsvorlagen untersuchen. Unter SVP-Typisch verstehe ich Initiativen, die entweder gegen die Zuwanderung oder gegen die Öffnung gegenüber der EU sind. Ausserdem Referenden gegen Asylgesetzreformen, bei denen das Asylgesetz gelockert wurde und Referenden gegen die Vereinfachung der Einbürgerung. Damit möchte ich sehen, in was für Gemeinden solche Vorlagen besonders gut ankommen und wie sich das in den letzten 50 Jahren verändert hat.

Dazu schaue ich die Abstimmungsresultate an, aber auch die Bevölkerungsentwicklung der Gemeinden und schaue, ob und was für einen Zusammenhang es z. B. mit der Bevölkerungsentwikclung oder dem Ausländer*innenanteil gibt.

## Data source

Folgende Abstimmungresultate:

- 2020-09-27 Volksinitiative «Für eine massvolle Zuwanderung» 
- 2019-05-19 Bundesbeschluss über die Genehmigung und die Umsetzung des Notenaustauschs zwischen der Schweiz und der EU betreffend die Übernahme der Richtlinie (EU) 2017/853 zur Änderung der EU-Waffenrichtlinie (Weiterentwicklung des Schengen-Besitzstands)
- 2018-11-25 Volksinitiative «Schweizer Recht statt fremde Richter (Selbstbestimmungsinitiative)»
- 2017-02-12 Bundesbeschluss über die erleichterte Einbürgerung von Personen der dritten Ausländergeneration
- 2016-06-05 Änderung des Asylgesetzes (AsylG)
- 2016-02-28 Volksinitiative «Zur Durchsetzung der Ausschaffung krimineller Ausländer (Durchsetzungsinitiative)»
- 2014-11-30 Volksinitiative «Stopp der Überbevölkerung - zur Sicherung der natürlichen Lebensgrundlagen»
- 2014-02-09 Volksinitiative «Gegen Masseneinwanderung»
- 2013-06-09 Asylgesetz (AsylG) (Dringliche Änderungen des Asylgesetzes)
- 2012-06-17 Volksinitiative «Für die Stärkung der Volksrechte in der Aussenpolitik (Staatsverträge vors Volk!)»
- 2010-11-28 Ausschaffungsinitiative und Gegenvorschlag: Stichfrage
- 2010-11-28 Bundesbeschluss über die Aus- und Wegweisung krimineller Ausländerinnen und Ausländer im Rahmen der Bundesverfassung (Gegenentwurf zur Ausschaffungsinitiative)
- 2010-11-28 Volksinitiative «Für die Ausschaffung krimineller Ausländer»
- 2009-11-29 Volksinitiative «Gegen den Bau von Minaretten»
- 2006-09-24 Änderung des Asylgesetzes
- 2006-09-24 Bundesgesetz über die Ausländerinnen und Ausländer
- 2005-09-25 Bundesbeschluss über die Ausdehnung des Personenfreizügigkeitsabkommens auf die neuen EU-Staaten und über die Revision der flankierenden Massnahmen
- 2005-06-05 Bundesbeschluss über die Genehmigung und die Umsetzung der bilateralen Abkommen zwischen der Schweiz und der EU über die Assoziierung an Schengen und Dublin
- 2004-09-26 Bundesbeschluss über den Bürgerrechtserwerb von Ausländerinnen und Ausländern der dritten Generation
- 2004-09-26 Bundesbeschluss über die ordentliche Einbürgerung sowie über die erleichterte Einbürgerung junger Ausländerinnen und Ausländer der zweiten Generation
- 2002-11-24 Volksinitiative «gegen Asylrechtsmissbrauch»
- 2001-03-04 Volksinitiative «Ja zu Europa!»
- 1999-06-13 Bundesbeschluss über dringliche Massnahmen im Asyl- und Ausländerbereich
- 1999-06-13 Asylgesetz
- 1996-12-01 Volksinitiative «gegen die illegale Einwanderung»
- 1992-12-06 Bundesbeschluss über den Europäischen Wirtschaftsraum (EWR)
- 1988-12-04 Volksinitiative «für die Begrenzung der Einwanderung»
- 1984-05-20 Volksinitiative «gegen den Ausverkauf der Heimat»
- 1977-03-13 Volksinitiative «IV. Ueberfremdungsinitiative» (1. Initiative wurde 1968 zurückgezogen)
- 1974-10-20 Volksinitiative «gegen die Ueberfremdung und Ueberbevölkerung der Schweiz»
- 1970-06-07 Volksinitiative «gegen die Ueberfremdung»

## Data Collection

Die Abstimmungsresultate pro Gemeinde sind seit 1960 auf der Gemeindeebene verfügbar und können hier heruntergeladen werden:
https://www.pxweb.bfs.admin.ch/pxweb/de/px-x-1703030000_101/px-x-1703030000_101/px-x-1703030000_101.px

Die Datei ist als csv unter `data/px-x-17030300000_101.csv` abgelegt, sie enthält für jede der gewählten Abstimmungen und Gemeinde der Schweiz:
- Name und Datum der Vorlage
- Die Anzahl der Stimmberechtigten
- Die total abgegebenen Stimmen
- Die Stimmbeteiligung in Prozent
- Die Anzahl der gültigen Stimmen
- Anzahl der JA Stimmen
- Anzahl der NEIN Stimmen
- Die JA Stimmen in Prozent

Um die Abstimmungsergebnisse in Kontext zu den Gemeinden zu stellen, verwenden wir die Bilanz der ständigen Wohnbevölkerung nach Bezirken und Gemeinden, 1991-2019:
https://www.bfs.admin.ch/bfs/de/home/statistiken/kataloge-datenbanken/tabellen.assetdetail.13707341.html
In der Datei: `data/su-d-01.02.04.07.xlsx`, sie umfasst für jede Gemeinde und für die Jahre 1991 - 2019:
- Die Bevölkerungsstand am 1. Januar
- Die Geburten
- Todesfälle
- Geburtenüberschuss
- Die Zuzüge und Wegüzge sowie den Wanderungssaldo
- Bestandesbereinigungen
- Den Bevölkerungsstand am 31. Dezember
- Die Veränderung absolut und in Prozent


und die in der Datei `data/su-d-01.02.04.09.xlsx` Bilanz der ständigen ausländischen Wohnbevölkerung nach Bezirken und Gemeinden, 1991-2019. Die selben Spalten wie bei der ständigen Wohnbevölkerung, aber noch mit einer zusätzlichen Spalte für die Anzahl der Erwerbe des Schweizer Bürgerrechts.

https://www.bfs.admin.ch/bfs/de/home/statistiken/kataloge-datenbanken/tabellen.assetdetail.13707411.html

https://www.bfs.admin.ch/bfs/de/home.assetdetail.11587763.html
