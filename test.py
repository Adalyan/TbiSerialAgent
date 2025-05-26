
import requests

def controller():
    url = 'http://192.168.1.8:5129/ports/COM2/'
    try:
        res = requests.get(url, timeout=8000)
        print("result:",res)
    except Exception as e:
        print(e)



if __name__ == '__main__':
    controller()