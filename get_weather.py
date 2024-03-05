import requests
import json

api_key = 'cde2fcfca5966aeec3658751726d8f99'
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city_name = "Stockholm"
complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&units=metric"
response = requests.get(complete_url)
x = response.json()

#GLOBALS

y = x["main"]
print(y)
current_temp = y["temp"]
max_temp = round((y["temp_max"]))
min_temp = round(y["temp_min"])
humidity = y["humidity"]
pressure = y["pressure"]
feels = y["feels_like"]




def get_temp():
    return(str(current_temp)+" °C")


def get_temp_min():
    return(str(min_temp)+" °C")


def get_temp_max():
    return(str(max_temp)+" °C")

def get_humidity():
    return(str(humidity))

def get_pressure():
    return(str(pressure))

def get_feel():
    return(str(feels)+"°C")
