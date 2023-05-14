import requests, sqlite3
from requests.auth import HTTPBasicAuth
import json, time, pytz #anturidata

from datetime import datetime

con = sqlite3.connect("lampo.db3")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS lampo (aika STRING PRIMARY KEY, finnanturi INTEGER, piirianturi INTEGER)")
con.commit()
con.close

while True:
    response = requests.get('https://tie.digitraffic.fi/api/weather/v1/stations/10014/data/',
            auth = HTTPBasicAuth('digitraffic', 'digitrafficPassword'))
    # Tulee muodossa requests.models.Response.
    # Muunnetaan sanakirjaksi.
    testi = response.json()

    lampo = testi['sensorValues']
    lampo1 = lampo[0]
    lampo2 = lampo1['value']
    print(lampo2)

    aikav = pytz.timezone("Europe/Helsinki")
    now = datetime.now(aikav)

    current_time = now.strftime("%d/%m/%y | %H.%M")
    current_timeS = now.strftime("%d/%m/%y | %H.%M.%S")
    #current_time = float(current_time)
    print(type(current_time))
    # Lämpöarvo piirilevyltä.
    #piiri = anturidata()
    
    # Käytä tätä, jos piirilevy ei ole kytketty.
    # Muista myös kommentoida import anturidata pois
    piiri = 5

    # Arvot sanakirjaan.
    s = {}
    s['alfa'] = current_time
    s['x'] = lampo2
    s['y'] = piiri

    print(s)
    con = sqlite3.connect("lampo.db3")
    cur = con.cursor()
    cur.execute("INSERT INTO lampo (aika, finnanturi, piirianturi) VALUES (?,?,?)",
        (current_timeS, lampo2, piiri))
    con.commit()
    con.close

    res = cur.execute("SELECT finnanturi FROM lampo")
    print(res.fetchall())
    
    ss = json.dumps(s)
    print(ss)

    response = requests.post("http://localhost:5000/uusimittaus", data = ss)

    time.sleep(5)