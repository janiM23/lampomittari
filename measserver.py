import json
from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO, emit
import json

# Flask ja socketio.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Lista mittauksia varten
measurements = []

# Näytä mittaukset Google Chart -kaavion avulla
@app.route('/')
def get_line():
    return render_template('linechart.html', result = measurements)

# Otetaan vastaan HTTP POSTilla lähetty mittaus ja laitetaan se listaan
@app.route('/uusimittaus', methods=['POST'])
def new_meas():
    # luetaan data viestistä ja deserialisoidaan JSON-data
    m = request.get_json(force=True)
    # muutetaan mittaus Google Chartille sopivaan muotoon (sanakirja -> lista)
    
    mg = [m['alfa'], m['x'], m['y']]

    # laitetaan listamuotoinen mittaus taulukkoon
    measurements.append(mg)
    # lähetetään koko taulukko socket.io:n avulla html-sivulle

    viimeiset_mittaukset = measurements

    # [-5:] näyttää viisi viimeisintä arvoa sivulla
    s = json.dumps(measurements[-5:])
    socketio.emit('my_response', {'result': s})
    # palautetaan vastaanotettu tieto
    return json.dumps(m, indent=True)

if __name__ == '__main__':
    socketio.run(app)
   