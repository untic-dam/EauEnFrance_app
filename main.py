import functions as f
import streamlit as st
import pandas as pd


global insee, ville, code_bss

st.write("""
# Les eaux souterraines en France

Avec cette application web vous allez pouvoir extraire les niveaux piézométriques de plusieurs stations d'observations françaises
""")

st.sidebar.header('Recherche')

#1 recupère le code postal ou nom de ville
user_request = st.sidebar.text_input('CODE POSTAL ou NOM DE LA VILLE', 'Wolfisheim')

#2 recupere le code INSEE associe au code potal ou au nom de la ville
insee, ville = f.recup_code_insee(user_request)

#3 recupere la liste des stations situées dans la ville
station_req, stations = f.recup_list_stations(insee, ville)

#4 afficher les stations
#get liste stations et nbr de mesure
list_stations = f.extrait_list_stations_to_selectbox(stations)

#5selection de la station
station_lbl = st.sidebar.selectbox(
                'Selectionner la station',
                list_stations)

#extraction du code bss
station_code = station_lbl.split(' | ')[0]

#fetch la station à partir du code selectionné
station = f.fetch_station(stations, station_code)

#6 affiche la station selectionnée
station_loc = f.station_to_map(station)
st.map(station_loc)

#7 recupère la chronique
code_bss = st.sidebar.text_input('code bss :', station['code_bss']) 
chronique_req, chroniques = f.recup_chronique(code_bss)

#8 Afficher la piezo
#transformation chroniques -> df time series
#chroniques (list) -> df
df_chronique_brut = pd.DataFrame(chroniques)
# df -> .csv
df_chronique_brut.to_csv('data.csv', index=False)
# csv -> df time series
df_chronique = pd.read_csv('data.csv', index_col='date_mesure', parse_dates=True)

#plot
attribut = st.sidebar.selectbox(
                "Selectionner l'attribut ",
                ['niveau_nappe_eau', 'profondeur_nappe'])
resample_size = st.sidebar.selectbox(
                "moyenne",
                ['Y', '6M', 'M', 'W', 'D'])
fig = f.matplot_piezo(df_chronique, attribut, resample_size)
st.pyplot(fig)

#9 telecharger data
st.sidebar.markdown(f.filedownload(df_chronique, ville, code_bss), unsafe_allow_html=True)


