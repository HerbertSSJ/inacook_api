import requests
from django.shortcuts import render, redirect
from django.contrib import messages

API_USUARIOS = "http://127.0.0.1:8000/api/usuarios/"
API_PASSWORD = "http://127.0.0.1:8000/api/cambiar-password/"


def dashboard(request):
    return render(request, "dashboard.html")

def calculadora(request):
    return render(request, "calculadora.html")

def perfil_view(request):
    user_id = request.session.get("user_id")

    if not user_id:
        messages.error(request, "Debes iniciar sesión")
        return redirect("login")

    response = requests.get(f"{API_USUARIOS}{user_id}/")
    usuario = response.json() if response.status_code == 200 else {}

    if request.method == "POST":
        data = {
            "username": request.POST.get("username"),
            "email": request.POST.get("email"),
        }

        update = requests.put(f"{API_USUARIOS}{user_id}/", json=data)

        if update.status_code == 200:
            messages.success(request, "Datos actualizados")
            return redirect("perfil")
        else:
            messages.error(request, "Error al actualizar datos")

    return render(
        request,
        "perfil.html",
        {"usuario": usuario}
    )


def cambiar_password(request):
    if request.method == "POST":
        data = {
            "password": request.POST.get("password"),
        }

        response = requests.post(API_PASSWORD, json=data)

        if response.status_code == 200:
            messages.success(request, "Contraseña actualizada")
            return redirect("perfil")
        else:
            messages.error(request, "Error al cambiar contraseña")

    return render(request, "cambiar_password.html")

