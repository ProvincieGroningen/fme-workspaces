Het komt voor dat bronsystemen geen mutatiehistorie bijhouden, terwijl dit wel wenselijk is. Dit prototype is ontwikkeld om mutatiehistorie op te bouwen in een feature class in de Enterprise Geodatabase. Het prototype gaat ervan uit dat de bron eveneens een feature class is, maar dat zal in werkelijkheid waarschijnlijk niet zo zijn. De workspace is daar echter eenvoudig op aan te passen.

In de historie wordt nooit een feature verwijderd. Verwijderde features worden afgesloten. Ze krijgen een `DATUM_VERVALLEN`. Van gewijzigde features wordt de oude versie afgesloten en een nieuwe aangemaakt.

Het prototype gaat ervan uit dat iedere feature in het bronsysteem een uniek `ENTITEIT_ID` heeft.

Een feature heeft in de historie drie extra attributen ten opzichte van het bronsysteem:
* `MUTATIE_ID`
* `DATUM_AANGEMAAKT`
* `DATUM_VERVALLEN`

De workspace is gemaakt in FME Desktop 2016 en getest met ArcGIS 10.3.1 en Oracle 10g.

Voor demonstratie- en testdoeleinden zijn twee ESRI Workspace documenten toegevoegd. Hiermee kunnen de feature classes geïmporteerd worden die nodig zijn om de FME workspace uit te voeren.

Uit de historie kunnen met een eenvoudige query de actuele gegevens gefilterd worden:

`SELECT *`     
`FROM INCLUSIEF_HISTORIE`     
`WHERE DATUM_VERVALLEN IS NULL`     

De gegevens op een bepaalde peildatum, bijvoorbeeld 1-6-2018, vraag je als volgt op:

`SELECT *`     
`FROM INCLUSIEF_HISTORIE`     
`WHERE DATUM_OPGEVOERD < to_date('2018-06-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS) AND`     
`     (DATUM_VERVALLEN >= to_date('2018-06-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS) OR DATUM_VERVALLEN IS NULL)`     