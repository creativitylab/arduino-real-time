import serial
import json
from time import time
from flask import render_template, make_response, Flask, request, jsonify

# ser = serial.Serial("COM6", 9600)
from serial import SerialException

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecretkey"

global ser


@app.before_first_request
def do_something_only_once():
    global ser
    ser = serial.Serial("COM6", 9600)
    app.logger.info("Created connection with Arduino")


@app.route('/', methods=['GET', 'POST'])
def index():
    # ser = serial.Serial("COM6", 9600)

    if request.method == 'POST':
        if request.form.get('ON') == 'ON':
            print('light ON')
            ser.write(b'H')
            print('turning led ON')
            pass  # do something
        elif request.form.get('OFF') == 'OFF':
            print('light OFF')
            # time.sleep(4)
            ser.write(b'L')
            print('turning led OFF')
            pass  # do something else
        else:
            pass  # unknown

    return render_template('Main.html')


@app.route('/humidity', methods=['GET'])
def humidity():

    # ser = serial.Serial("COM6", 9600)
    while True:
        temperature = ser.read(5).decode('utf-8')

        humidity = ser.read(5).decode('utf-8')

        print('humidity ', float(humidity))
        # print('random temperature type ', type(temp))

        data = [time() * 1000, float(humidity), time() * 1000, float(temperature)]

        print('humidity ', humidity)
        print('temperature ', temperature)
        try:
            temperature = [time() * 1000, float(temperature)]
            humidity = [time() * 1000, float(humidity)]
        except ValueError:
            print('value error')
            temperature = [time() * 1000, 22.4]
            humidity = [time() * 1000, 55.50]

        response = make_response(json.dumps(data))
        response.content_type = 'application/json'
        return jsonify(results=[temperature, humidity])
        # return response


if __name__ == '__main__':
    app.run(debug=True)
