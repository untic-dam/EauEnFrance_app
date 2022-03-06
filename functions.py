import requests

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