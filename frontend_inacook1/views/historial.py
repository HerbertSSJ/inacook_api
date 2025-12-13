import requests
from django.shortcuts import render
from django.contrib import messages

API_HISTORIAL = "http://127.0.0.1:8000/api/historial/"

def ver_historial(request):
    response = requests.get(API_HISTORIAL)

    if response.status_code == 200:
        historial = response.json()
    else:
        historial = []
        messages.error(request, "No se pudo cargar el historial")

    return render(
        request,
        "ver_historial.html",
        {"historial": historial}
    )


