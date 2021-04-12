from django.shortcuts import render, redirect
import requests
from datetime import date

def paginacion(data, offset):
    data_nueva = data
    offset = offset
    while True:
        URL = 'https://tarea-1-breaking-bad.herokuapp.com/api/characters?limit=10&offset='+str(offset)
        data = requests.get(URL) 
        data = data.json() 
        if len(data)== 0:
            break
        else:
            offset+=10
            data_nueva +=data
            return paginacion(data_nueva, offset)
            
    return data_nueva

def current_date_format(date):
    months = ("Enero", "Febrero", "Marzo", "Abri", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
    day = date.day
    month = months[date.month - 1]
    year = date.year
    messsage = "{} de {} del {}".format(day, month, year)
    return messsage
    
def inicio(request):
    print("SOLICITANDO INFORMACION DE INTERNET")
    print("espere....") 
    URL1 = 'https://tarea-1-breaking-bad.herokuapp.com/api/episodes?series=Better+Call+Saul'
    URL2 = 'https://tarea-1-breaking-bad.herokuapp.com/api/episodes?series=Breaking+Bad' #configuramos la url
    #solicitamos la información y guardamos la respuesta en data.
    data1 = requests.get(URL1) 
    data1 = data1.json() 

    data2 = requests.get(URL2) 
    data2 = data2.json() 

    Temporadas_BCL = {}
    Temporadas_BB = {}
    for element in data1: #iteramos sobre data
        Temporadas_BCL[element["season"]] = (element["title"])
    for element in data2: #iteramos sobre data
        Temporadas_BB[element["season"]] = (element["title"])
    context = {
        "serie1": "BETTER CALL SAUL",
        "serie2": "BREAKING BAD",
        "temporadas_bcl": Temporadas_BCL,
        "temporadas_bb": Temporadas_BB
    }
    return render(request, "index.html", context)

def episodios(request, serie, temporada):
   
    nombre_serie = "+".join(serie.split(" "))
    URL = 'https://tarea-1-breaking-bad.herokuapp.com/api/episodes?series='+nombre_serie
    data = requests.get(URL) 
    data = data.json()
    Episodios = []
    for element in data: #iteramos sobre data
        if int(element["season"]) == temporada:
            Episodios.append(element)
    context = {
        "serie": serie,
        "serie1": "BETTER CALL SAUL",
        "serie2": "BREAKING BAD",
        "temporada": temporada,
        "episodios": Episodios
    }

    return render(request, "episodios.html", context)
   

def datos_episodio(request, serie, episodio):
    id_episodio = str(episodio)
    print(id_episodio)
    URL = 'https://tarea-1-breaking-bad.herokuapp.com/api/episodes/'+id_episodio
    data = requests.get(URL) 
    data = data.json()
    print(data)
    for i in range(len(data)): #iteramos sobre data
        element = data[i]
        fecha = element["air_date"][:10]
        fecha= date(int(fecha[:4]), int(fecha[5:7]), int(fecha[8::]))
        data[i]["air_date"] = current_date_format(fecha)
    
    context = {
        "serie": serie,
        "serie1": "BETTER CALL SAUL",
        "serie2": "BREAKING BAD",
        "episodio": data[0]
    }
    return render(request, "datos_episodio.html", context)
    
def datos_personaje(request, personaje):
    nombre_personaje = "+".join(personaje.split(" "))
    URL = 'https://tarea-1-breaking-bad.herokuapp.com/api/characters?name='+nombre_personaje
    URL2 = 'https://tarea-1-breaking-bad.herokuapp.com/api/quote?author='+nombre_personaje
    data = requests.get(URL) 
    data = data.json()
    citas = requests.get(URL2) 
    citas = citas.json()
    context = {
        "serie1": "BETTER CALL SAUL",
        "serie2": "BREAKING BAD",
        "personaje": data[0],
        "citas": citas
    }
    return render(request, "datos_personaje.html", context)

def buscar_personaje(request):
    print("estoy aca")
    if request.method == "POST":
        persona = request.POST['person']
        print(persona)
        persona = persona.lower()
        data = paginacion([], 0)
        caracteres = []
        print(data)
        for personaje in data:
            if persona in personaje["name"].lower():
                caracteres.append(personaje)
        print(caracteres)
        context = {
            "serie1": "BETTER CALL SAUL",
            "serie2": "BREAKING BAD",
            "busqueda": persona,
            "personajes": caracteres
        }
        return render(request, "lista_personajes.html", context)
    else:
        return inicio(request)
        


    
    
