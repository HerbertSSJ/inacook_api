import requests
from django.shortcuts import render, redirect
from django.contrib import messages

API_LOGIN = "http://127.0.0.1:8000/api/token-auth/"

def login_view(request):
    if request.method == "POST":
        data = {
            "username": request.POST.get("nombre"),
            "password": request.POST.get("contraseña"),
        }

        response = requests.post(API_LOGIN, data=data)

        if response.status_code == 200:
            token = response.json().get("token")

            request.session["token"] = token
            request.session["username"] = data["username"]
            
            try:
                resp_users = requests.get(API_REGISTER)
                if resp_users.status_code == 200:
                    users = resp_users.json()
                    current_user = next((u for u in users if u['username'] == data['username']), None)
                    
                    if current_user:
                        request.session['user_id'] = current_user['id']
                        rol_data = current_user.get('rol')
                        if isinstance(rol_data, dict):
                             request.session['rol_nombre'] = rol_data.get('nombre')
                        else:
                             request.session['rol_nombre'] = "Estudiante"
                             
                             if isinstance(rol_data, int):
                                 r_resp = requests.get(API_ROLES)
                                 if r_resp.status_code == 200:
                                     roles_list = r_resp.json()
                                     r_obj = next((r for r in roles_list if r['id'] == rol_data), None)
                                     if r_obj:
                                         request.session['rol_nombre'] = r_obj.get('nombre')

            except Exception as e:
                print(f"Error fetching user details: {e}")

            messages.success(request, "Sesión iniciada correctamente")
            return redirect("dashboard")

        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, "login.html")


API_REGISTER = "http://127.0.0.1:8000/api/usuarios/"
API_ROLES = "http://127.0.0.1:8000/api/roles/"

def register_view(request):
    roles = []
    
    try:
        resp_roles = requests.get(API_ROLES)
        if resp_roles.status_code == 200:
            roles = resp_roles.json()
    except Exception:
        roles = []

    if request.method == "POST":

        selected_rol = request.POST.get("rol")
        rol_id = None
        if selected_rol:
            try:
                rol_id = int(selected_rol)
            except Exception:
                rol_id = None

        
        if rol_id is None:
            for r in roles:
                if r.get("nombre") and r.get("nombre").lower() == "estudiante":
                    rol_id = r.get("id")
                    break

        data = {
            "username": request.POST.get("nombre"),
            "password": request.POST.get("contraseña"),
            "email": request.POST.get("correo"),
            "rol": rol_id
        }

        response = requests.post(API_REGISTER, json=data)

        if response.status_code in [200, 201]:
            messages.success(request, "Usuario creado correctamente")
            return redirect("login")
        else:
            messages.error(request, "Error al crear usuario")

    return render(request, "register.html", {"roles": roles})


def logout_view(request):
    request.session.flush()
    messages.success(request, "Sesión cerrada")
    return redirect("login")
