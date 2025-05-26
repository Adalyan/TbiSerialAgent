import json
import os
import sys
import time
from datetime import datetime

import serial
import glob
import sys
from cryptography.fernet import Fernet
import logging


logger=logging.getLogger(__name__)

def load_key():
    return "IEAWNjjAxtaEosg-AgJBmtgEehYBhqjwjYZzrntQK4Y="


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return (d2 - d1).days


def encrypt(message):
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message


def decrypt(encrypted_message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message.decode()


def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def check_int(str):
    if str[0] in ('-', '+'):
        return str[1:].isdigit()
    return str.isdigit()


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


def read_data(prt):
    from interpreter import read_settings_for_device
    settings = read_settings_for_device(prt)
    ser = serial.Serial(prt, baudrate=settings["baud_rate"], timeout=0, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE)
    ser.xonxoff = 1

    try:
        ser.close()
    except Exception as err:
        logger.error(err)
    ser.open()
    time.sleep(1)
    line = []
    ct = 0
    # ser.write(b'P')
    while ct < 6000:
        rline = ser.readline()
        # if rline != b'':
        #     line.append(rline.decode('utf-8', 'slashescape'))
        line.append(rline.decode(encoding="ISO-8859-1"))
        # line.append(rline.decode(encoding="utf-8"))
        ct += 1
    ser.close()
    rs = ""
    for i in line:
        rs += i
    # print(rs)
    return rs
