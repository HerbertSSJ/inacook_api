import requests
from django.shortcuts import render, redirect
from django.contrib import messages

API_INGREDIENTES = "http://127.0.0.1:8000/api/ingredientes/"
API_UNIDADES = "http://127.0.0.1:8000/api/unidades/"


def crear_ingrediente(request):
    resp_u = requests.get(API_UNIDADES)
    unidades_data = resp_u.json() if resp_u.status_code == 200 else []
    
    choices = [(u['id'], f"{u['Nombre_Unidad']} ({u['Abreviatura']})") for u in unidades_data]

    if request.method == "POST":
        form = IngredienteForm(request.POST, unidades_choices=choices)
        
        if form.is_valid():
            data = {
                "nombre": form.cleaned_data['Nombre_Ingrediente'],
                "calidad": form.cleaned_data['Calidad'],
                "costo_unitario": form.cleaned_data['Costo_Unitario'],
                "unidad_medicion": form.cleaned_data['UnidadMedicion']
            }
            
            resp = requests.post(API_INGREDIENTES, json=data)
            
            if resp.status_code == 201:
                messages.success(request, "Ingrediente creado correctamente")
                return redirect('ver_ingredientes')
            else:
                messages.error(request, "Error al crear ingrediente en API")
    else:
        form = IngredienteForm(unidades_choices=choices)

    return render(request, "crear_ingrediente.html", {"form": form})


def ver_ingredientes(request):
    response = requests.get(API_INGREDIENTES)
    ingredientes = response.json() if response.status_code == 200 else []

    resp_u = requests.get(API_UNIDADES)
    unidades = resp_u.json() if resp_u.status_code == 200 else []
    
    unit_map = {u['id']: u for u in unidades}
    
    for ing in ingredientes:
        u_id = ing.get('unidad_medicion')
        if u_id and u_id in unit_map:
            u_obj = unit_map[u_id]
            ing['unidad_nombre'] = u_obj.get('nombre', 'Unknown')
            ing['unidad_abreviatura'] = u_obj.get('abreviatura', '')
        else:
            ing['unidad_nombre'] = "Sin unidad"
            ing['unidad_abreviatura'] = ""

    return render(
        request,
        "ver_ingredientes.html",
        {"ingredientes": ingredientes}
    )


def eliminar_ingrediente(request, id):
    requests.delete(f"{API_INGREDIENTES}{id}/")
    messages.success(request, "Ingrediente eliminado")
    return redirect('ver_ingredientes')


def editar_ingrediente(request, id):
    resp_i = requests.get(f"{API_INGREDIENTES}{id}/")
    if resp_i.status_code != 200:
        messages.error(request, "Ingrediente no encontrado")
        return redirect('ver_ingredientes')
    
    ingrediente = resp_i.json()
    
    resp_u = requests.get(API_UNIDADES)
    unidades_data = resp_u.json() if resp_u.status_code == 200 else []
    choices = [(u['id'], f"{u['Nombre_Unidad']} ({u['Abreviatura']})") for u in unidades_data]

    initial_data = {
        'Nombre_Ingrediente': ingrediente.get('Nombre_Ingrediente', ingrediente.get('nombre')),
        'Calidad': ingrediente.get('Calidad', ingrediente.get('calidad')),
        'Costo_Unitario': ingrediente.get('Costo_Unitario', ingrediente.get('costo_unitario')),
        'UnidadMedicion': ingrediente.get('UnidadMedicion')
    }
    if isinstance(initial_data['UnidadMedicion'], dict):
         initial_data['UnidadMedicion'] = initial_data['UnidadMedicion'].get('id')

    if request.method == "POST":
        form = IngredienteForm(request.POST, unidades_choices=choices)
        if form.is_valid():
            data = {
                "nombre": form.cleaned_data['Nombre_Ingrediente'],
                "calidad": form.cleaned_data['Calidad'],
                "costo_unitario": form.cleaned_data['Costo_Unitario'],
                "unidad_medicion": form.cleaned_data['UnidadMedicion']
            }
            
            resp = requests.put(f"{API_INGREDIENTES}{id}/", json=data)
            
            if resp.status_code == 200:
                messages.success(request, "Ingrediente actualizado")
                return redirect('ver_ingredientes')
            else:
                messages.error(request, "Error al actualizar ingrediente")
    else:
        form = IngredienteForm(unidades_choices=choices, initial=initial_data)

    return render(request, "editar_ingrediente.html", {
        "form": form,
        "ingrediente": ingrediente
    })
