import requests
from django.shortcuts import render, redirect
from django.contrib import messages

API_USUARIOS = "http://127.0.0.1:8000/api/usuarios/"
API_PASSWORD = "http://127.0.0.1:8000/api/cambiar-password/"


def dashboard(request):
    if not request.session.get('token'):
        return redirect('login')
        
    return render(request, "dashboard.html", {
        "nombre": request.session.get('username', 'Usuario'),
        "rol": request.session.get('rol_nombre', 'Estudiante')
    })

def calculadora(request):
    return render(request, "calculadora.html")

def perfil_view(request):
    user_id = request.session.get("user_id")

    if not user_id:
        messages.error(request, "Debes iniciar sesión")
        return redirect("login")

    response = requests.get(f"{API_USUARIOS}{user_id}/")
    usuario = response.json() if response.status_code == 200 else {}

    # resolver nombre del rol para mostrar en la plantilla
    rol_nombre = None
    try:
        # caso: serializer expone 'nombre_rol' en la respuesta
        if usuario.get('nombre_rol'):
            rol_nombre = usuario.get('nombre_rol')
        else:
            # caso: 'rol' es un objeto con 'nombre'
            rol = usuario.get('rol')
            if isinstance(rol, dict) and rol.get('nombre'):
                rol_nombre = rol.get('nombre')
            elif isinstance(rol, int):
                # buscar en API de roles
                resp_roles = requests.get(API_ROLES)
                if resp_roles.status_code == 200:
                    roles = resp_roles.json()
                    r = next((x for x in roles if x.get('id') == rol), None)
                    if r:
                        rol_nombre = r.get('nombre')
    except Exception:
        rol_nombre = None

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
        {"usuario": usuario, "rol_nombre": rol_nombre}
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

