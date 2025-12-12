from django.shortcuts import render
import requests

Api_url = "http://127.0.0.1:8000/api/"

def home(request):
    return render(request, "home.html")

def ver_recetas(request):
    response = requests.get(Api_url + "recetas/")
    recetas = response.json() if response.status_code == 200 else []
    return render(request, "ver_recetas.html", {"recetas": recetas})

def ver_ingredientes(request):
    response = requests.get(Api_url + "ingredientes/")
    ingredientes = response.json() if response.status_code == 200 else []
    return render(request, "ver_ingredientes.html", {"ingredientes": ingredientes})

def ver_historial(request):
    response = requests.get(Api_url + "historial/")
    historial = response.json() if response.status_code == 200 else []
    return render(request, "ver_historial.html", {"historial": historial})

def editar_receta(request, id):
    response = requests.get(Api_url + "recetas/" + str(id) + "/")
    receta = response.json() if response.status_code == 200 else {}
    return render(request, "editar_receta.html", {"receta": receta})

