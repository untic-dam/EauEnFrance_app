import functions as f
import streamlit as st
import time 


st.write("""
# Les eaux souterraines en France

Avec cette application web vous allez pouvoir extraire les niveaux piézométriques de plusieurs stations d'observations françaises
""")

#1 recupère le code postal 
code_postal = st.text_input('CODE POSTAL', '67000')

#2 recupere le code INSEE associe au code potal
insee, ville, population = f.recup_commune(code_postal)

#3 recupere la liste des stations situées dans la ville
station_req, stations = f.recup_list_stations(insee, ville)

#4 afficher les stations

#5 choisir une stations
station = f.station_max_mesure(stations)

# affiche la station selectionnée
station_loc = f.station_to_map(station)
st.map(station_loc)

