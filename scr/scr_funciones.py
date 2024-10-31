#Función para crear un df con nombre, lat y lon
import pandas as pd
import numpy as np
import requests
from tqdm import tqdm
from time import sleep
import os
import dotenv
dotenv.load_dotenv()


from geopy.geocoders import Nominatim


def convertir_df(lista_mun):
    lista_dic=[]
    for municipio in tqdm(lista_mun):
        geolocator = Nominatim(user_agent="my_application")
        location = geolocator.geocode(municipio)
        dicc=location.raw
        lista_dic.append(dicc)
    df= pd.DataFrame(lista_dic)
    return df[["name","lat","lon"]]


def query_fsq(url, latitud, longitud, id_categoria):

    params= {
        "ll": ""+str(latitud)+","+str(longitud),
        "categories": id_categoria,
        "radius": 10000,
        "sort":"DISTANCE"
    }
    key= os.getenv("token")
    headers = {
        "accept": "application/json",
        "Authorization": key
    }
    response = requests.request("GET",url, params= params, headers=headers)
    datos = response.json()
    return datos




def obtener_df(result):
    dict_resultados = dict()
    df_final = pd.DataFrame()
    for i in result["results"]:
        dict_resultados["Nombre"] = i["name"]
        dict_resultados["Direccion"] = i["location"]["formatted_address"]
        dict_resultados["Categoria"] = i["categories"][0]["name"]

        df_resultado = pd.DataFrame([dict_resultados])
        df_final = pd.concat([df_final, df_resultado])

    return df_final