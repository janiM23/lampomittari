import requests, sqlite3
from requests.auth import HTTPBasicAuth
import json, time, pytz #anturidata

from datetime import datetime

# Tietokanta.
con = sqlite3.connect("lampo.db3")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS lampo (aika STRING PRIMARY KEY, finnanturi INTEGER, piirianturi INTEGER)")
con.commit()
con.close

# Toistolause lämpötila-arvoille.

while True:
    response = requests.get('https://tie.digitraffic.fi/api/weather/v1/stations/10014/data/',
            auth = HTTPBasicAuth('digitraffic', 'digitrafficPassword'))
    # Tulee muodossa requests.models.Response.
    # Muunnetaan sanakirjaksi.
    testi = response.json()

    # Ronkitaan sanakirjasta oikea arvo muuttujaan.
    lampo = testi['sensorValues']
    lampo1 = lampo[0]
    lampo2 = lampo1['value']

    # Otetaan oikea aikaleima aikavyöhykkeen mukaan.
    aikav = pytz.timezone("Europe/Helsinki")
    now = datetime.now(aikav)

    # Sidotaan aikaleimat kahteen muuttujaan.
    # current_timeS käytetään tietokannassa tarkkuuden vuoksi.
    # current_time esitetään google chartissa.
    current_time = now.strftime("%d/%m/%y | %H.%M")
    current_timeS = now.strftime("%d/%m/%y | %H.%M.%S")

    # Lämpöarvo piirilevyltä.
    #piiri = anturidata()

    # Käytä tätä, jos piirilevy ei ole kytketty.
    # !!Muista myös kommentoida import anturidata pois!!
    piiri = 5

    # Arvot sanakirjaan.
    s = {}
    s['alfa'] = current_time
    s['x'] = lampo2
    s['y'] = piiri

    # Lisätään arvot tietokantaan.
    con = sqlite3.connect("lampo.db3")
    cur = con.cursor()
    cur.execute("INSERT INTO lampo (aika, finnanturi, piirianturi) VALUES (?,?,?)",
        (current_timeS, lampo2, piiri))
    con.commit()
    con.close
    
    # json-muunnosa ja post.
    ss = json.dumps(s)
    response = requests.post("http://localhost:5000/uusimittaus", data = ss)

    # Tämän voi vaihtaa sen mukaan kuinka nopeasti halutaan uudet arvot.
    time.sleep(10)