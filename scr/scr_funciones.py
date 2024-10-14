#Función para crear un df con nombre, lat y lon
def convertir_df(lista_mun):
    lista_dic=[]
    for municipio in tqdm(lista_mun):
        geolocator = Nominatim(user_agent="my_application")
        location = geolocator.geocode(municipio)
        dicc=location.raw
        lista_dic.append(dicc)
    df= pd.DataFrame(lista_dic)
    return df[["name","lat","lon"]]