import requests
from django.shortcuts import render
from django.contrib import messages

API_HISTORIAL = "http://127.0.0.1:8000/api/historial/"

from django.utils.dateparse import parse_datetime

def ver_historial(request):
    response = requests.get(API_HISTORIAL)

    if response.status_code == 200:
        historial = response.json()
        for h in historial:
            if h.get('fecha_modificacion'):
                h['fecha_modificacion'] = parse_datetime(h['fecha_modificacion'])
        
        historial.sort(key=lambda x: x['fecha_modificacion'] if x.get('fecha_modificacion') else parse_datetime('1900-01-01T00:00:00Z'), reverse=True)
    else:
        historial = []
        messages.error(request, "No se pudo cargar el historial")

    return render(
        request,
        "ver_historial.html",
        {"historial": historial}
    )


