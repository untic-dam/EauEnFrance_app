import requests
import pandas as pd
import matplotlib.pyplot as plt
import base64


def recup_commune_code_postal(code_postal):
    #addresse api
    curl = f'https://geo.api.gouv.fr/communes?codePostal={str(code_postal)}'
    #requete api
    commune_req = requests.get(curl).json()
    
    #json
    commune = commune_req[0]
    
    #info
    insee = commune['code']
    ville = commune['nom']
    
    return insee, ville


def recup_commune_nom_ville(nom_ville):
    #addresse api
    #curl 'https://geo.api.gouv.fr/communes?nom=Carcassonne&fields=departement&boost=population&limit=5'
    curl = f'https://geo.api.gouv.fr/communes?nom={str(nom_ville)}&fields=departement&boost=population&limit=5'
    #requete api
    commune_req = requests.get(curl).json()
    
    #json
    commune = commune_req[0]
    
    #info
    insee = commune['code']
    ville = commune['nom']
    
    return insee, ville


def recup_code_insee(user_request):
    ville_par_defaut = 'Colmar' 
    ville_inconnue = False
    code_postal_inconnue = False

    #essaye code postal
    try:
        insee, ville = recup_commune_code_postal(user_request)
    except:
        code_postal_inconnue = True

    #essaye nom ville
    try:
        insee, ville = recup_commune_nom_ville(user_request)
    except:
        ville_inconnue = True

    #permet de gérer nom de ville et departement inconnue
    if (code_postal_inconnue and ville_inconnue) == True:
        insee, ville = recup_commune_nom_ville(ville_par_defaut)
        print(f'code postal ou nom de ville inconnue. \nville par défaut : {ville_par_defaut}\n')
        
    return insee, ville


def recup_list_stations(insee, ville):
    code_insee_defaut = '68066' #Colmar
    #code de la ville
    insee_str = str(insee)
    #url pour la requete
    station_url = f'https://hubeau.eaufrance.fr/api/v1/niveaux_nappes/stations?code_commune={insee_str}&format=json&size=20&pretty'
    station_req = requests.get(station_url).json()
    #list des stations piezometriques
    stations = station_req['data']

    if len(stations) == 0:
        print("Impossible de récupérer des stations dans cette ville")
        print("choix par defaut : ",code_insee_defaut)
        #on récupère la ville par defaut
        station_url = f'https://hubeau.eaufrance.fr/api/v1/niveaux_nappes/stations?code_commune={code_insee_defaut}&format=json&size=20&pretty'
        station_req = requests.get(station_url).json()
        #list des stations piezometriques
        stations = station_req['data']
    
    return station_req, stations


def station_max_mesure(stations):
    mesure_max = 0
    code_bss = ''
    station = {}

    for s in stations:
        mesures = s['nb_mesures_piezo']
        if mesures > mesure_max:
            mesure_max = mesures
            code_bss = s['code_bss']
            station = s
    
    print(f"la station {code_bss} possède le plus de mesure avec {mesure_max} mesures.")
    
    return station


def return_df_stations(stations):
    df_stations = pd.DataFrame(stations)
    #colonnes pertinentes
    cols = ['code_bss', 'nb_mesures_piezo']
    df_stations_light = df_stations[cols]
    #tri dans l'ordre croisant
    df_stations_light.sort_values(by='nb_mesures_piezo', ascending=False, inplace=True)
    #reset index pour être afficher correctement dans st.selectbox
    df_stations_light.reset_index(drop=True, inplace=True)

    return df_stations_light

def extrait_list_stations_to_selectbox(stations):

    df_stations_light = return_df_stations(stations)

    #loop pour creer les labels à afficher dans selectbox
    list_stations = []
    for i in df_stations_light.index:
        code = df_stations_light.iloc[i,0]
        n_mesure = df_stations_light.iloc[i,1]

        txt = f"{code} | {n_mesure} mesures"

        list_stations.append(txt)

    return list_stations

def fetch_station(stations, station_code):
    #permet de retourner la station correspondant au code_bss dans une list de stations 

    station = {}
    for s in stations:
        if s['code_bss'] == station_code:
            station = s
    
    return station



def station_to_map(station):
    cols = ['x', 'y']

    df_station = pd.DataFrame(station, index=[0])
    df_station = df_station[cols]
    df_station.rename(columns={'x':'lon'}, inplace=True)
    df_station.rename(columns={'y':'lat'}, inplace=True)
    
    return df_station


def recup_chronique(code_bss, size=5000):
    
    chronique_url = f'https://hubeau.eaufrance.fr/api/v1/niveaux_nappes/chroniques?code_bss={code_bss}&size={str(size)}'

    chronique_req = requests.get(chronique_url).json()
    chroniques = chronique_req['data']
    print(f"il y a {len(chroniques)} mesure(s)")
    
    return chronique_req, chroniques


def matplot_piezo(df_chronique, attribut='profondeur_nappe', resample_size='Y'):
    #extract data
    nappe = df_chronique[attribut].resample(resample_size).agg(['mean', 'std', 'min', 'max'])
    #define series
    x = nappe.index
    y = nappe['mean'].values
    y_min = nappe['min'].values
    y_max = nappe['max'].values
    #plot
    fig, ax = plt.subplots()
    ax.plot(x, y, label=attribut)
    ax.fill_between(x, y_min, y_max, alpha=0.2, label='min-max')
    ax.legend()

    return fig


def filedownload(df, ville, code_bss):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    fn = f'piezo_{ville}_{code_bss}.csv'.replace('/','_')
    href = f'<a href="data:file/csv;base64,{b64}" download="{fn}">Telecharger au format CSV</a>'
    return href