import base64
import threading
import zlib

import flask
from flask import Flask, jsonify, request
from flask_cors import cross_origin
from werkzeug.serving import make_server

import simplejson as json

from fnc import pp_json, read_data, serial_ports
from interpreter import read_lines, read_lines_for_device, process_command_on_raw
from OpenSSL import SSL

api_address = "0.0.0.0"
api_port = 5129
api = Flask(__name__)
from flask_cors import CORS
import logging
import socket

logger = logging.getLogger(__name__)
CORS(api, resources=[r'/api/*', r'/auth/*'], origins=[r'^https://.*xxxx\.org$'], supports_credentials=True,
     vary_header=True)


@api.route('/', methods=['POST', 'GET'])
def home():
    s = ""
    s += api_address + ":" + str(api_port) + "<br/>"
    s += 'TBI Serial Agent API server V0.1<br />'
    return s


@api.route('/ports/')
def ports():
    return json.dumps(serial_ports())

@api.route('/sockets/<device_ip>/', methods=['POST', 'GET'])
@cross_origin()
def sockets(device_ip):
    raw = ""
    try:
        TCP_IP = device_ip.split(':')[0]
        TCP_PORT = int(device_ip.split(':')[1])
        BUFFER_SIZE = 1024
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        raw = s.recv(BUFFER_SIZE).decode("utf-8")
        # print(raw)
        s.close()
        lines = read_lines_for_device(device_ip)
        for line in lines:
            raw = process_command_on_raw(raw, line)
    except Exception as err:
        print(err)
    return flask.Response(raw)

@api.route('/ports/<device_name>/', methods=['POST', 'GET'])
@cross_origin()
def device(device_name):
    try:
        if device_name == "test1":
            raw = """A 0
            C 200
            C 50
            A 100
            """
        else:
            raw = read_data(device_name)
        lines = read_lines_for_device(device_name)
        for line in lines:
            raw = process_command_on_raw(raw, line)
        resp = flask.Response(raw)
        return resp
    except Exception as err:
        logger.error(err)
        print(err)
    return flask.Response("error")


class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        from interpreter import read_settings_for_device
        settings = read_settings_for_device("global")
        if settings.get("ssl") == "on":
            import ssl
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(certfile="./tbi_serial_cert.pem", keyfile="./tbi_serial_key.pem")
            context.load_default_certs()
        else:
            context = None
        self.srv = make_server(host=api_address, port=api_port, app=api, threaded=True, ssl_context=context)
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
