import streamlit as st
import plotly.graph_objects as go
from utils import *
import time
import pandas as pd
import numpy as np
from datetime import datetime
from PIL import Image
from streamlit_autorefresh import st_autorefresh
from streamlit_folium import folium_static
import folium
import requests
import matplotlib.pyplot as plt
import requests
import json
from windrose import WindroseAxes
from matplotlib.backends.backend_pdf import PdfPages

st.set_page_config(page_title="Agrifirm@AquaSim", layout="wide")

readme = load_config("config_readme.toml")


# Info
st.title("AquaSim Project")


########################login################################
# Função para carregar imagem
def load_image(image_path):
    return Image.open(image_path)

def main():
    # Página de login
    st.sidebar.image(load_image("logo2.png"), use_column_width=True)


##############################fazendas e barra lateral#######################################

# Add the select bar in the sidebar
st.sidebar.image(load_image("logo.png"), use_column_width=True)
display_links(readme["links"]["repo"], readme["links"]["other_link"])

with st.sidebar:
    st.write("When choosing the farm below, the data on the main page will be updated to that of the farm.")
    farm_choice = st.selectbox("Select your farm", ("farm1", "farm2"))

# Create a container in the main section for the weather data
st.write("Weather Data")
container = st.container()

# fazendas que serao usadas no AquaSim
if farm_choice == "farm1":
    farm_geojson_path = "/home/salles/Documents/streamlit/aquasim/farms/farm1.geojson"
    latitude, longitude = 52.7691942697887, 6.445785619296203
    farm_zoom = 15  # Zoom level for farm1
elif farm_choice == "farm2":
    farm_geojson_path = "/home/salles/Documents/streamlit/aquasim/farms/farm2.geojson"
    latitude, longitude = 52.771922, 6.442589
    farm_zoom = 15  # Zoom level for farm2
    
    
############################soil map########################################


st.write("Mapa de solo")

# Display the map in the central part of the page
farm_map = folium.Map(location=[latitude, longitude], zoom_start=farm_zoom)

# Try to load and display the GeoJson file
try:
    with open(farm_geojson_path, 'r') as f:
        data = f.read()
    folium.GeoJson(data).add_to(farm_map)
    folium_static(farm_map)
except ValueError:
    st.write("Cannot render the selected farm.")


##############################################OpenWeatherMap#################################

api_key = 'cde2fcfca5966aeec3658751726d8f99'
base_url = "http://api.openweathermap.org/data/2.5/forecast?"

complete_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
#https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={APIkey}
#complete_url = base_url + q= + city_name + "&appid=" + api_key
#complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&units=metric"
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
#sea = round(y["sea_level"])



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
    
    

#Autorefresh:
#count = st_autorefresh(interval=5000, limit=100, key="fizzbuzzcounter")


################data e imagem do clima######################

import streamlit as st
from datetime import datetime

#Time
nowTime = datetime.now()
current_time = nowTime.strftime("%H:%M:%S")
today = datetime.today().strftime("Day - %d/%m/%Y")

# Obter o ícone do clima e a descrição
weather_icon = x['weather'][0]['icon']
weather_description = x['weather'][0]['description']

# Abrir a imagem correspondente ao ícone do clima
image_path = f"icons/{weather_icon}.png"
img = Image.open(image_path)

# Criar duas colunas
col1, col2 = st.columns(2)

# Exibir a imagem na primeira coluna
col2.image(img, width=115)

# Exibir o campo de data na segunda coluna
col1.metric("", today)

# Adicionar uma linha horizontal
st.markdown('<hr style="border-top: 1px solid #f63366">', unsafe_allow_html=True)

################i######################

# Row A
with st.container():
    a1, a2 = st.columns(2)
    a1.metric("Temperature", f"{get_temp()}")
    a2.metric("Time", current_time)

# Row B
with st.container():
    b1, b2 = st.columns(2)
    b1.metric("Humidity", f"{get_humidity()}"+"%")
    b2.metric("Feels like", f"{get_feel()}")

# Row C
with st.container():
    c1, c2 = st.columns(2)
    c1.metric("Highest temperature", f"{get_temp_max()}")
    c2.metric("Lowest temperature", f"{get_temp_min()}")



################grafico com forecast de 5 dias ################################


import streamlit as st
import requests
import plotly.graph_objects as go

# URL da API
complete_url_forecast = f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&appid={api_key}&units=metric&exclude=current,minutely,hourly,alerts"

# Request
response_forecast = requests.get(complete_url_forecast)

# JSON
z = response_forecast.json()

# Forecast
forecast = z["daily"]

# Dias da semana
days = [forecast[i]["dt"] for i in range(5)]

# Temperaturas
temperatures = [forecast[i]["temp"]["day"] for i in range(5)]
min_temperatures = [forecast[i]["temp"]["min"] for i in range(5)]
max_temperatures = [forecast[i]["temp"]["max"] for i in range(5)]

# Figura
fig = go.Figure()

# Temperatura média
fig.add_trace(go.Scatter(
    x=days,
    y=temperatures,
    mode='lines',
    name='Average Temperature',
    line=dict(color='black')
))

# Temperatura mínima
fig.add_trace(go.Scatter(
    x=days,
    y=min_temperatures,
    mode='lines',
    name='Minimum Temperature',
    line=dict(color='rgb(26, 118, 255)')
))

# Temperatura máxima
fig.add_trace(go.Scatter(
    x=days,
    y=max_temperatures,
    mode='lines',
    name='Maximum Temperature',
    line=dict(color='rgb(255, 65, 54)')
))

# Layout
fig.update_layout(
    title='Forecast Temperatures for Next 5 Days',
    xaxis=dict(
        title='Day of Week',
        titlefont_size=16,
        tickfont_size=14,
        tickvals=days,
        ticktext=[datetime.utcfromtimestamp(day).strftime('%A') for day in days]
    ),
    yaxis=dict(
        title='Temperature (C)',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
)

# Gráfico
st.plotly_chart(fig, use_container_width=True)


###############################botao de reflesh#######################

#Manually refresh button
st.button("Update the above weather data")

########################################################temperature pelo VisualCrossing###################################

import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px

def Get_Weather(farmername,farmname,latitude,longitude):
    farmername = str(farmername)
    farmname = str(farmname)
    latitude = str(latitude)
    longitude = str(longitude)
    
    api_key = 'NPW6A94TU9EY7USZ65ZGJS9C9'

    url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'+latitude+'%2C'+longitude+'?unitGroup=metric&key='+api_key+'&contentType=json'

    r = requests.get(url)

    data = r.json()

    # Top Section: Overview
    st.subheader(f'Location: {data["resolvedAddress"]}')
    st.subheader(f'Timezone: {data["timezone"]}')

    # Next 15 Days Temperature
    st.header("Next 15 Days Temperature")
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[day['datetime'] for day in data['days']],
        y=[day['tempmin'] for day in data['days']],
        name='Minimum',
        marker_color='black'
    ))

    fig.add_trace(go.Bar(
        x=[day['datetime'] for day in data['days']],
        y=[day['temp'] for day in data['days']],
        name='Average',
        marker_color='rgb(26, 118, 255)'
    ))

    fig.add_trace(go.Bar(
        x=[day['datetime'] for day in data['days']],
        y=[day['tempmax'] for day in data['days']],
        name='Maximum',
        marker_color='rgb(255, 65, 54)'
    ))

    fig.update_layout(
        title='Next 15 Days Temperature',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Temperature (C)',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1  # gap between bars of the same location coordinate.
    )

    st.plotly_chart(fig, use_container_width=True)

    # prec
    dew = [day['precip'] for day in data['days']]
    fig = px.line(x=[day['datetime'] for day in data['days']], y=dew, title='Precipitation - Next 15 Days')
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Precipitation (mm)')
    st.plotly_chart(fig, use_container_width=True)


    # Dew
    dew = [day['dew'] for day in data['days']]
    fig = px.line(x=[day['datetime'] for day in data['days']], y=dew, title='Dew Point - Next 15 Days')
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Dew (C)')
    st.plotly_chart(fig, use_container_width=True)

    # Humidity
    humidity = [day['humidity'] for day in data['days']]
    fig = px.line(x=[day['datetime'] for day in data['days']], y=humidity, title='Air Humidity - Next 15 Days')
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Humidity (%)')
    st.plotly_chart(fig, use_container_width=True)
    
    # Solar Radiation
    solarradiation = [day['solarradiation'] for day in data['days']]
    fig = px.line(x=[day['datetime'] for day in data['days']], y=solarradiation, title='24 Hours Solar Radiation Data')
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Solar Radiation')
    st.plotly_chart(fig, use_container_width=True)
    
    # Visibility
    visibility = [day['visibility'] for day in data['days']]
    fig = px.line(x=[day['datetime'] for day in data['days']], y=visibility, title='24 Hours Visibility Data')
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Visibility')
    st.plotly_chart(fig, use_container_width=True)


    # Wind Speed
    windspeed = [day['windspeed'] for day in data['days']]
    winddir = [day['winddir'] for day in data['days']]
    fig = go.Figure()
    fig.add_trace(go.Barpolar(
        r=windspeed,
        theta=winddir,
        name='Wind Speed',
        marker_color='rgb(55, 83, 109)'
    ))
    fig.update_layout(
        title='Wind Speed (Km/h)',
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(windspeed)]
            )
        ),
        showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)

    # Pressure
    pressure = [day['pressure'] for day in data['days']]
    fig = px.line(x=[day['datetime'] for day in data['days']], y=pressure, title='24 Hours Pressure Data')
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Pressure (Pa)')
    st.plotly_chart(fig, use_container_width=True)


    # Sun Data
    sundata = [[day['datetime'], (datetime.fromtimestamp(day['sunriseEpoch']).strftime('%H:%M:%S')),
                (datetime.fromtimestamp(day['sunsetEpoch']).strftime('%H:%M:%S'))] for day in data['days']]
    sundata.insert(0, ["DATE", "SUN RAIS", "SUN SET"])
    fig = go.Figure(data=[go.Table(header=dict(values=["DATE", "SUN RAIS", "SUN SET"]), cells=dict(values=sundata))])
    st.plotly_chart(fig, use_container_width=True)


    # Cloud Cover
#    cloudcover = [day['cloudcover'] for day in data['days']]
#    fig = go.Figure()
#    fig.add_trace(go.Pie(
#        labels=[f"Date: {day['datetime']}" for day in data['days']],
#        values=cloudcover,
#        title='15 Days Cloud Cover Data',
#        textinfo='label+percent',
#        hole=.3,
#        marker=dict(
#            colors=px.colors.sequential.RdBu
#        )
#    ))
#    st.plotly_chart(fig, use_container_width=True)



###########################side bar##########################################



container.text_input("Latitude:", value=latitude)
container.text_input("Longitude:", value=longitude)

if st.button("Click here to have a complete weather forecast for the next 15 days"):
    Get_Weather("Farmer Name", "Farm Name", latitude, longitude)
    
###########################soil moisture by csv file############################

# Carregar os dados do arquivo CSV
df = pd.read_csv("soil-moisture.csv")

def plot_soil_moisture():
    # Criar o gráfico com Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['VWC_15_Agurotech'], mode='lines', name='VWC_15_Agurotech'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['VWC_30_Agurotech'], mode='lines', name='VWC_30_Agurotech'))

    fig.update_layout(title='Soil Moisture Values',
                      xaxis_title='Date',
                      yaxis_title='Soil Moisture',
                      template='plotly_dark')

    # Exibir o gráfico
    st.plotly_chart(fig)
    
###############################irrigation#######################

# Carregar os dados do arquivo CSV
df_irrigation = pd.read_csv("irrigation.csv", parse_dates=['Day'])

def plot_irrigation_needs():
    # Criar o gráfico de barras com Plotly Express
    fig = px.bar(df_irrigation, x='Day', y='Irrigation', title='Irrigation Needs Forecast',
                 labels={'Day': 'Date', 'Irrigation (mm)': 'Irrigation Needs'},
                 template='plotly_dark')

    # Exibir o gráfico
    st.plotly_chart(fig)

# Botão para mostrar o gráfico
if st.button("Irrigation Needs Forecast"):
    plot_irrigation_needs()

# Botão para mostrar o gráfico
if st.button("CRITERIA-1D Soil Moisture Values"):
    plot_soil_moisture()    
    
######################################################

if __name__ == "__main__":
    main()

