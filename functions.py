import requests
import pandas as pd
import matplotlib.pyplot as plt

def recup_commune(code_postal):
    #addresse api
    curl = f'https://geo.api.gouv.fr/communes?codePostal={str(code_postal)}'
    #requete api
    commune_req = requests.get(curl).json()
    
    #json
    commune = commune_req[0]
    
    #info
    insee = commune['code']
    ville = commune['nom']
    population = commune['population']
    
    return insee, ville, population


def recup_list_stations(insee, ville):
    #code de la ville
    insee_str = str(insee)
    #url pour la requete
    station_url = f'https://hubeau.eaufrance.fr/api/v1/niveaux_nappes/stations?code_commune={insee_str}&format=json&size=20&pretty'
    station_req = requests.get(station_url).json()
    #list des stations piezometriques
    stations = station_req['data']

    print(f"il y a {len(stations)} station(s) à {ville}")
    
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