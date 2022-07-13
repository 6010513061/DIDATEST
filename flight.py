import requests
from datetime import datetime,time,date
class get_api(object):
    def api(self):
        # d = date.today()
        url = "https://aerodatabox.p.rapidapi.com/flights/airports/icao/VTSS/2022-07-12T07:00/2022-07-12T18:00"
        querystring = {"withLeg":"true","withCancelled":"true","withCodeshared":"true","withCargo":"true","withPrivate":"true","withLocation":"false"}

        headers = {
        	"X-RapidAPI-Key": "4ff001bc68msh34909c4e588cec4p1aa676jsn1ae1c79cac53",
        	"X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        j = response.json()
        return j

    def api2(self):
        d = date.today()
        url2 = "https://aerodatabox.p.rapidapi.com/flights/airports/icao/VTSS/{t}T18:01/{t}T22:50".format(t=d)
        querystring = {"withLeg":"true","withCancelled":"true"
        ,"withCodeshared":"true","withCargo":"true","withPrivate":"true","withLocation":"false"}

        headers = {
        	"X-RapidAPI-Key": "4ff001bc68msh34909c4e588cec4p1aa676jsn1ae1c79cac53",
        	"X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
        }

        response = requests.request("GET", url2, headers=headers, params=querystring)
        n = response.json()
        # print(respose.text)
        return n
