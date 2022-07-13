import requests
import http.client
from datetime import datetime,date


conn = http.client.HTTPSConnection("airport-info.p.rapidapi.com")

date_now = date.today()
headers = {
    'X-RapidAPI-Key': "SIGN-UP-FOR-KEY",
    'X-RapidAPI-Host': "airport-info.p.rapidapi.com"
    }

conn.request("GET", "/airport?iata=HDY", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
# api ariport shcedules hdy
url = "https://airport-on-time-performance.p.rapidapi.com/airport/predictions/on-time"

querystring = {"date":"{td}".format(td=date_now),"airportCode":"HDY"}

headers = {
	"X-RapidAPI-Key": "SIGN-UP-FOR-KEY",
	"X-RapidAPI-Host": "airport-on-time-performance.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)
print("api:",response.text)

import http.client

conn = http.client.HTTPSConnection("airport-info.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "SIGN-UP-FOR-KEY",
    'X-RapidAPI-Host': "airport-info.p.rapidapi.com"
    }

conn.request("GET", "/airport?iata=HDY", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
