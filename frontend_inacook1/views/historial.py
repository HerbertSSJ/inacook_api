import requests
from django.shortcuts import render
from django.contrib import messages

API_HISTORIAL = "http://127.0.0.1:8000/api/historial/"
API_USUARIOS = "http://127.0.0.1:8000/api/usuarios/"

from django.utils.dateparse import parse_datetime

def ver_historial(request):
    
    headers = {}
    token = request.session.get('token')
    if token:
        headers['Authorization'] = f'Token {token}'

    
    usuarios = []
    try:
        resp_users = requests.get(API_USUARIOS, headers=headers)
        usuarios = resp_users.json() if resp_users.status_code == 200 else []
    except Exception:
        usuarios = []

    
    params = {}
    usuario_id = request.GET.get('usuario_id')
    if usuario_id:
        params['usuario_id'] = usuario_id

    try:
        response = requests.get(API_HISTORIAL, headers=headers, params=params)
    except Exception:
        response = None

    if response is not None and response.status_code == 200:
        historial = response.json()
        for h in historial:
            if h.get('fecha_modificacion'):
                h['fecha_modificacion'] = parse_datetime(h['fecha_modificacion'])
        
        historial.sort(key=lambda x: x['fecha_modificacion'] if x.get('fecha_modificacion') else parse_datetime('1900-01-01T00:00:00Z'), reverse=True)
    else:
        historial = []
        messages.error(request, "No se pudo cargar el historial")

    current_user_id = request.session.get('user_id')
    is_profesor = False
    try:
        me = next((u for u in usuarios if u.get('id') == current_user_id), None)
        nombre_rol = (me.get('nombre_rol') or '').lower() if me else ''
        if nombre_rol and ('profesor' in nombre_rol or 'teacher' in nombre_rol or 'admin' in nombre_rol or 'administrador' in nombre_rol):
            is_profesor = True
    except Exception:
        is_profesor = False

    
    alumnos = []
    for u in usuarios:
        rol = (u.get('nombre_rol') or '').lower()
        if 'alumno' in rol or 'estudiante' in rol or u.get('rol') == 2:
            alumnos.append(u)

    return render(
        request,
        "ver_historial.html",
        {
            "historial": historial,
            "alumnos": alumnos,
            "is_profesor": is_profesor,
            "selected_usuario_id": usuario_id
        }
    )


