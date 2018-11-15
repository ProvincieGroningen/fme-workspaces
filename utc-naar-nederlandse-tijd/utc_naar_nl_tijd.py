import fme
import fmeobjects
import math
from datetime import date, datetime, timedelta
 
# Dit script zet datum en tijd in UTC om in Nederlandse tijd, rekening houdend met winter- en zomertijd.
#
# Ron Wardenier
# 2018-01-03: creatie
# 2018-01-04: gewijzigd: "T" uit datum-tijd notatie gehaald.
# 2018-01-12: tijdstip overgang gecorrigeerd en code netter gemaakt
#
# Code gebaseerd op http://www.staff.science.uu.nl/~gent0113/wettijd/wettijd.htm
#
 
# Deze functie is nodig omdat in FME de python module 'locale' niet goed werkt
def vind_dag_naam(week_dag_nummer):
    dag_namen = ['maandag', 'dinsdag', 'woensdag', 'donderdag', 'vrijdag', 'zaterdag', 'zondag']
    dag_naam = dag_namen[week_dag_nummer]
    return dag_naam.capitalize()
 
# Deze functie is nodig omdat in FME de python module 'locale' niet goed werkt
def vind_maand_naam(maand_nummer):
    maand_namen = ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'oktober', 'november', 'december']
    maand_naam = maand_namen[maand_nummer - 1]
    return maand_naam
 
 
# Template Function interface:
# When using this function, make sure its name is set as the value of
# the 'Class or Function to Process Features' transformer parameter
def processFeature(feature):
    logger = fmeobjects.FMELogFile()
    # Lees attribuut waarden voor datum en tijd en neem aan dat die in UTC zijn
    utc_datum_event = feature.getAttribute('date')
    utc_tijd_event = feature.getAttribute('time')
    utc_datum_tijd_event = datetime.strptime(str(utc_datum_event)+' '+str(utc_tijd_event), "%Y-%m-%d %H:%M:%S")
    jaar = utc_datum_tijd_event.year
    a = math.floor(5 * int(jaar) / 4)
    b = math.floor(int(jaar) / 100)
    c = math.floor(int(jaar) / 400)
    f = (a - b + c) % 7
    # Bereken datum van ingang zomertijd (is eerste dag van zomertijd periode)
    eerste_dag_zomertijd = 31 - (f + 5) % 7
    datum_eerste_dag_zomertijd = str(int(jaar)) + '-03-' + str(int(eerste_dag_zomertijd))
    # Bereken datum van ingang wintertijd (is eerste dag van wintertijd periode)
    eerste_dag_wintertijd = 31 - (f + 2) % 7
    datum_eerste_dag_wintertijd = str(int(jaar)) + '-10-' + str(int(eerste_dag_wintertijd))
    # Bepaal de begin en eind tijdstippen van de overgangen in UTC
    # Het moment van ingang is altijd om 01 uur UTC
    utc_datum_tijd_eerste_dag_zomertijd = datetime.strptime(datum_eerste_dag_zomertijd + " 01:00", "%Y-%m-%d %H:%M")
    utc_datum_tijd_eerste_dag_wintertijd = datetime.strptime(datum_eerste_dag_wintertijd+" 01:00", "%Y-%m-%d %H:%M")
    # Bepaal of het tijdstip in de zomertijd periode ligt
    if utc_datum_tijd_eerste_dag_zomertijd < utc_datum_tijd_event < utc_datum_tijd_eerste_dag_wintertijd:
        # Zomertijd, dus tel een extra uur bij UTC op en stel zomertijd aanduidingen in
        nl_datum_tijd_event = utc_datum_tijd_event + timedelta(hours = 2)
        aanduiding1 = 'MEZT'
        aanduiding2 = '(zomertijd)'
    else:
        # Wintertijd, dus tel een uur bij UTC op (MET=UTC+1) en stel wintertijd aanduidingen in
        nl_datum_tijd_event = utc_datum_tijd_event + timedelta(hours = 1)
        aanduiding1 = 'MET'
        aanduiding2 = '(wintertijd)'
    # Leesbare versie van lokale datum en tijd
    dag = str(nl_datum_tijd_event.day)
    dag_naam = vind_dag_naam(nl_datum_tijd_event.weekday())
    maand_naam = vind_maand_naam(nl_datum_tijd_event.month)
    jaar = str(nl_datum_tijd_event.year)
    # Beperk tijd tot uren en minuten. NB geen afronding om verschillen in datum te voorkomen.
    tijd = format(nl_datum_tijd_event, '%H.%M')
    # Maak extra attribuut data (let op de optie Attributes to Expose in de PythonCaller transformer!)
    feature.setAttribute('datumtijd_nl', format(nl_datum_tijd_event, '%Y-%m-%d %H:%M:%S') + ' ' + aanduiding1)
    feature.setAttribute('datumtijd_nl_mooi', dag_naam + ', ' + dag+ ' ' + maand_naam+ ' ' + jaar + ' ' + tijd + ' uur ' + aanduiding2)
    feature.setAttribute('jaar', jaar)
 
