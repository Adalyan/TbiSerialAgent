import evdev
from evdev import InputDevice, categorize, ecodes
import serial
import RPi.GPIO as GPIO
import os, time
import sys
import pyodbc
import serial
import glob
import barcode_session

dev = InputDevice('/dev/input/event0')

def get_any_usb_port():
    first_port = None
    ports = glob.glob('/dev/ttyUSB[0-9]*')
    for port in ports:
        try:
            first_port = port
        except:
            pass
    print(first_port)
    return first_port

def read_data(prt):
    GPIO.setmode(GPIO.BOARD)
    ser = serial.Serial(prt, baudrate=9600, timeout=0, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE)
    ser.xonxoff=1

    try:
        ser.close()
    except:
        pass
    ser.open()
    time.sleep(1)
    line = []
    ct=0
    ser.write(b'P')
    while ct<6000:
        rline = ser.readline()
        if rline != b'':
            line.append(rline.decode('utf-8', 'slashescape'))
        ct+=1

    ser.close()

    rs = ""
    for i in line:
        rs += i
    print(rs)
    return rs

def insert_data2db(rs, auth_barcode, barcode):
    for i in rs.split("\n"):
        if i[1:6] == "GROSS":
            gross = rs.split("\n")[7].split("      ")[1].split(" ")[0]
        if i[1:3] == "CN":
            cn = rs.split("\n")[3].split(':')[1].strip()

    #auth_barcode = "prs0123456789" #auth_barcode[0:3]
    #barcode = "0123456789"
    conn = pyodbc.connect('DRIVER=FreeTDS;Server=192.168.1.5;PORT=1433;DATABASE=CENTER1;TDS_Version=7.2;')
    cursor = conn.cursor()
    cursor.execute("insert into KZLBASKUL(AUTH_BARCODE, BARCODE, CN, GROSS, READ_TIME) values (?, ?, ?, ?, GETDATE())", auth_barcode, barcode, cn, gross)
    cursor.commit()
    print("Inserted to DB")


scancodes = {
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'q', 17: u'w', 18: u'e', 19: u'r',
    20: u't', 21: u'y', 22: u'u', 23: u'i', 24: u'o', 25: u'p', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'a', 31: u's', 32: u'd', 33: u'f', 34: u'g', 35: u'h', 36: u'j', 37: u'k', 38: u'l', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'z', 45: u'x', 46: u'c', 47: u'v', 48: u'b', 49: u'n',
    50: u'm', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT'
}

capscodes = {
    0: None, 1: u'ESC', 2: u'!', 3: u'@', 4: u'#', 5: u'$', 6: u'%', 7: u'^', 8: u'&', 9: u'*',
    10: u'(', 11: u')', 12: u'_', 13: u'+', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'{', 27: u'}', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u':',
    40: u'\'', 41: u'~', 42: u'LSHFT', 43: u'|', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u'<', 52: u'>', 53: u'?', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT'
}

x = ''
caps = False

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
#buzzer=24
#GPIO.setup(buzzer,GPIO.OUT)
#GPIO.setmode(GPIO.BOARD)
#while True:
#  GPIO.output(buzzer,GPIO.HIGH)
    # print("sound 1")
    # time.sleep(0.5)
    #GPIO.output(buzzer,GPIO.LOW)
    #time.sleep(0.5)
   #print("sound")

dev.grab()

for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        data = categorize(event)
        if data.scancode == 42:
            if data.keystate == 1:
                caps = True
            if data.keystate == 0:
                caps = False
        if data.keystate == 1:
            if caps:
                key_lookup = u'{}'.format(capscodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(
                    data.scancode)  # Lookup or return UNKNOWN:XX
            else:
                key_lookup = u'{}'.format(scancodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(
                    data.scancode)  # Lookup or return UNKNOWN:XX
            if (data.scancode != 42) and (data.scancode != 28):
                x += key_lookup
            if data.scancode == 28:
                print(x)
                try:
                    if x[0:3] == "prs" :
                        barcode_session.last_auth_code = x
                        print("last")
                    else:
                        print("authorized!")
                        #if len(barcode_session.last_auth_code)>5:
                        if barcode_session.last_auth_code != "wait":
                            #auth_barcode = "prs0123456789" #auth_barcode[0:3]
                            #barcode = "0123456789"
                            barcode = str(x)
                            auth_barcode = str(barcode_session.last_auth_code)
                            try:
                                port = get_any_usb_port()
                                rs = read_data(port)
                                insert_data2db(rs, auth_barcode, barcode)
                            except Exception as erInside:
                                print(erInside)
                            barcode_session.last_auth_code = "wait"
                        else:
                            print("unauthorized access!")
                    x = ""
                except Exception as err:
                    print(err)
