import requests
from django.shortcuts import render
from django.contrib import messages

API_UNIDADES = "http://127.0.0.1:8000/api/unidades/"

def ver_unidades(request):
    response = requests.get(API_UNIDADES)

    if response.status_code == 200:
        unidades = response.json()
    else:
        unidades = []
        messages.error(request, "No se pudieron cargar las unidades de medida")

    return render(
        request,
        "ver_unidades.html",
        {"unidades": unidades}
    )

def editar_unidad(request, id):
    response = requests.get(f"{API_UNIDADES}{id}/")

    if response.status_code != 200:
        messages.error(request, "Unidad no encontrada")
        return redirect("ver_unidades")

    unidad = response.json()

    if request.method == "POST":
        data = {
            "nombre": request.POST.get("nombre"),
            "abreviatura": request.POST.get("abreviatura"),
        }

        update = requests.put(f"{API_UNIDADES}{id}/", json=data)

        if update.status_code == 200:
            messages.success(request, "Unidad actualizada correctamente")
            return redirect("ver_unidades")
        else:
            messages.error(request, "Error al actualizar la unidad")

    return render(
        request,
        "editar_unidad.html",
        {"unidad": unidad}
    )
