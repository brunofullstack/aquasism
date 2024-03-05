import streamlit as st
from time import sleep
from navigation import make_sidebar
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
from PIL import Image

st.set_page_config(page_title="Agrifirm@AquaSim", layout="wide")

def load_image(image_path):
    return Image.open(image_path)


make_sidebar()

st.title("Welcome to the Agrifirm@AquaSim project")


#st.write("Please log in to continue (username `test`, password `test`).")

# Lista de dicionários contendo usuários e senhas
users = [
    {"username": "test", "password": "test"},
    {"username": "filipe", "password": "filipe"},
    {"username": "user2", "password": "password2"}
]

# Entrada de nome de usuário e senha
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Verificação de login
if st.button("Log in", type="primary"):
    # Verifica se o nome de usuário e a senha correspondente estão no dicionário de usuários
    if any(user["username"] == username and user["password"] == password for user in users):
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/app.py")
    else:
        st.error("Incorrect username or password")

