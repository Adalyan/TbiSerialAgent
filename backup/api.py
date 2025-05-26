import base64
import glob
import sys
import threading
import zlib

import serial
from flask import Flask, jsonify,  request
from werkzeug.serving import make_server
# from barcode import get_any_usb_port
# from barcode import read_data
# from barcode import read_data
from data import fetch_data_asdict, fetch_grouped_data_asdict
import simplejson as json

from fnc import pp_json
# import serial.tools.list_ports
# ports = serial.tools.list_ports.comports()

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def get_any_usb_port():
    first_port = None
    # ports = glob.glob('/dev/ttyUSB[0-9]*')
    ports = glob.glob('/dev/*')
    for port in ports:
        try:
            first_port = port
        except:
            pass
    print(first_port)
    return first_port

api_address = "0.0.0.0"
api_port = 5129
api = Flask(__name__)

@api.route('/',  methods = ['POST', 'GET'])
def home():
    #s=""
    #s += api_address + ":" + str(api_port) +"<br/>"
    #s += 'TBI Serial Agent API server V0.1<br />'
    # port = get_any_usb_port()
    # rs = read_data(port)
    # print(serial_ports())
    # response = read_data("COM5", 9600)
    response = """A 0
    C 200
    C 50
    A 100
    """
    # response manipulation
    return response


class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.srv = make_server(api_address, api_port, api)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        print('starting server')
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()

def start_server():
    global server
    app = Flask('myapp')
    server = ServerThread(app)
    server.start()
    print('server started')

def stop_server():
    global server
    server.shutdown()
    print("server stopped")