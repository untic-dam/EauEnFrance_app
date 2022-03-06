import functions as f
import streamlit as st
import pandas as pd
import time 
import matplotlib.pyplot as plt


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

#get liste stations et nbr de mesure
#extrait la liste de stations sous forme d'un df
df_stations = pd.DataFrame(stations)
#colonnes pertinentes
cols = ['code_bss', 'nb_mesures_piezo']
df_stations_light = df_stations[cols]
#tri dans l'ordre croisant
df_stations_light.sort_values(by='nb_mesures_piezo', ascending=False, inplace=True)
#reset index pour être afficher correctement dans st.selectbox
df_stations_light.reset_index(drop=True, inplace=True)

#loop pour creer les labels à afficher dans selectbox
list_stations = []
for i in df_stations_light.index:
    code = df_stations_light.iloc[i,0]
    n_mesure = df_stations_light.iloc[i,1]

    txt = f"{code} | {n_mesure} mesures"

    list_stations.append(txt)

#selection de la station
station_lbl = st.selectbox(
        'Selectionner la station',
        list_stations)

#extraction du code bss
station_code = station_lbl.split(' | ')[0]

def fetch_station(stations, station_code):
    #permet de retourner la station correspondant au code_bss dans une list de stations 

    station = {}
    for s in stations:
        if s['code_bss'] == station_code:
            station = s
    
    return station

station = fetch_station(stations, station_code)
st.json(station)


