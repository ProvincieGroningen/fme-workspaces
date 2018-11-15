Een verkeersbesluit wordt digitaal bekendgemaakt via een officiële publicatie in de Staatscourant. De collectie officiële publicaties wordt als open data ontsloten via de [open data webservice van Overheid.nl](https://www.koopoverheid.nl/documenten/instructies/2018/03/24/handleiding-open-data-webservice-van-overheid.nl---sru).

Met het volgende request vraag je bijvoorbeeld alle verkeersbesluiten van de provincie Groningen op:

http://zoekdienst.overheid.nl/sru/Search?version=1.2&operation=searchRetrieve&x-connection=oep&startRecord=1&maximumRecords=1000&query=(keyword=verkeersbesluit)+and+(creator=groningen)+and+(organisationType=Provincie)

Met de workspace in deze map kunnen verkeersbesluiten van de provincie 'geharvest' worden. Hij is gemaakt in FME Desktop 2017.