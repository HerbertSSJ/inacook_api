import requests
from django.shortcuts import render, redirect
from django.contrib import messages

API_RECETAS = "http://127.0.0.1:8000/api/recetas/"
API_ALUMNOS = "http://127.0.0.1:8000/api/usuarios/"
API_RECETA_INGREDIENTE = "http://127.0.0.1:8000/api/receta-ingrediente/"
API_INGREDIENTES = "http://127.0.0.1:8000/api/ingredientes/"
API_UNIDADES = "http://127.0.0.1:8000/api/unidades/"

import json
from ..forms import RecetaForm

def get_auth_headers(request):
    token = request.session.get('token')
    return {'Authorization': f'Token {token}'} if token else {}

def subir_receta(request):
    if not request.session.get('token'):
        return redirect('login')

    headers = get_auth_headers(request)

    try:
        resp_ing = requests.get(API_INGREDIENTES)
        ingredientes = resp_ing.json() if resp_ing.status_code == 200 else []
        
        resp_uni = requests.get(API_UNIDADES)
        unidades = resp_uni.json() if resp_uni.status_code == 200 else []
    except:
        ingredientes = []
        unidades = []

    if request.method == "POST":
        form = RecetaForm(request.POST, request.FILES)
        
        if form.is_valid():
            data = {
                "nombre": form.cleaned_data['Nombre_Receta'], 
                "categoria": form.cleaned_data['Categoria'],
                "aporte_calorico": form.cleaned_data['Aporte_Calorico'],
                "tiempo_preparacion": form.cleaned_data['Tiempo_Preparacion'],
                "usuario": request.session.get("user_id")
            }
            
            files = {}
            if request.FILES.get('imagen'):
                files['imagen'] = request.FILES['imagen']

            if files:
                 response = requests.post(API_RECETAS, data=data, files=files, headers=headers)
            else:
                 response = requests.post(API_RECETAS, json=data, headers=headers)
            
            if response.status_code == 201:
                receta_id = response.json().get('id')
                
                ingredientes_json = request.POST.get('ingredientes_json')
                if ingredientes_json:
                    try:
                        lista_ing = json.loads(ingredientes_json)
                        for item in lista_ing:
                            ing_data = {
                                "receta": receta_id,
                                "ingrediente": int(item['id']),
                                "cantidad": float(item['cantidad'])
                            }
                            requests.post(API_RECETA_INGREDIENTE, json=ing_data, headers=headers)
                    except Exception as e:
                        print(f"Error procesando ingredientes: {e}")
                
                messages.success(request, "Receta creada exitosamente")
                return redirect('ver_recetas')
            else:
                messages.error(request, "Error al crear la receta en el servidor")
    else:
        form = RecetaForm()

    return render(request, "subir_receta.html", {
        "receta_form": form,
        "ingredientes": ingredientes,
        "unidades": unidades
    })

def editar_receta(request, id):
    if not request.session.get('token'):
        return redirect('login')
        
    headers = get_auth_headers(request)

    resp_r = requests.get(f"{API_RECETAS}{id}/", headers=headers)
    if resp_r.status_code != 200:
        messages.error(request, "Receta no encontrada")
        return redirect('ver_recetas')
    
    receta = resp_r.json()
    
    resp_ing = requests.get(API_INGREDIENTES, headers=headers)
    ingredientes_list = resp_ing.json() if resp_ing.status_code == 200 else []
    
    resp_uni = requests.get(API_UNIDADES, headers=headers)
    unidades_list = resp_uni.json() if resp_uni.status_code == 200 else []
    
    resp_rels = requests.get(API_RECETA_INGREDIENTE, headers=headers)
    all_rels = resp_rels.json() if resp_rels.status_code == 200 else []
    
    unit_map = {u['id']: u for u in unidades_list}
    
    for ing in ingredientes_list:
        u_id = ing.get('unidad_medicion')
        u_obj = unit_map.get(u_id)
        if u_obj:
            ing['unidad_abreviatura'] = u_obj.get('abreviatura')
        else:
            ing['unidad_abreviatura'] = ''
    
    receta_ingredientes = []
    
    ing_map = {i['id']: i for i in ingredientes_list}
    
    for rel in all_rels:
        if rel['receta'] == id:
            ing_obj = ing_map.get(rel['ingrediente'])
            if ing_obj:
                 mock_rel = {
                     'id': rel['id'], 
                     'Cantidad': rel['cantidad'],
                     'Ingrediente': ing_obj 
                 }
                 receta_ingredientes.append(mock_rel)

    initial_data = {
        'Nombre_Receta': receta.get('Nombre_Receta', receta.get('nombre')),
        'Categoria': receta.get('Categoria', receta.get('categoria')),
        'Aporte_Calorico': receta.get('Aporte_Calorico', receta.get('aporte_calorico')),
        'Tiempo_Preparacion': receta.get('Tiempo_Preparacion', receta.get('tiempo_preparacion')),
    }

    if request.method == "POST":
        form = RecetaForm(request.POST, request.FILES)
        if form.is_valid():
            data = {
                "nombre": form.cleaned_data['Nombre_Receta'],
                "categoria": form.cleaned_data['Categoria'],
                "aporte_calorico": form.cleaned_data['Aporte_Calorico'],
                "tiempo_preparacion": form.cleaned_data['Tiempo_Preparacion'],
                "usuario": receta.get('usuario')
            }
            
            requests.put(f"{API_RECETAS}{id}/", json=data, headers=headers)
            
            ingredientes_json = request.POST.get('ingredientes_json')
            if ingredientes_json:
                try:
                    for old_rel in receta_ingredientes:
                        requests.delete(f"{API_RECETA_INGREDIENTE}{old_rel['id']}/", headers=headers)
                    
                    lista_ing = json.loads(ingredientes_json)
                    for item in lista_ing:
                            ing_data = {
                                "receta": id,
                                "ingrediente": int(item['id']),
                                "cantidad": float(item['cantidad'])
                            }
                            requests.post(API_RECETA_INGREDIENTE, json=ing_data, headers=headers)
                            
                    messages.success(request, "Receta modificada exitosamente")
                    return redirect('ver_recetas')
                    
                except Exception as e:
                    print(e)
                    messages.error(request, "Error guardando ingredientes")
    
    else:
        form = RecetaForm(initial=initial_data)

    ingredientes_bd = {}
    for ing in ingredientes_list:
        ingredientes_bd[ing['id']] = {
            "nombre": ing['nombre'],
            "precio": ing['costo_unitario'],
            "calidad": ing['calidad'],
            "unidad": ing.get('unidad_abreviatura', '')
        }
    
    current_ingredientes = []
    for ri in receta_ingredientes:
        ing_obj = ri['Ingrediente']
        current_ingredientes.append({
            "id": ing_obj['id'],
            "nombre": ing_obj['nombre'],
            "cantidad": ri['Cantidad'],
            "unidad": ing_obj.get('unidad_abreviatura', ''),
            "precio": ing_obj['costo_unitario'],
            "calidad": ing_obj['calidad']
        })

    return render(request, "editar_receta.html", {
        "receta_form": form,
        "receta": receta,
        "ingredientes": ingredientes_list,
        "unidades": unidades_list,
        "receta_ingredientes": receta_ingredientes,
        "ingredientes_bd_json": json.dumps(ingredientes_bd),
        "receta_ingredientes_json": json.dumps(current_ingredientes)
    })

def borrar_receta(request, id):
    if not request.session.get('token'):
        return redirect('login')
    
    headers = get_auth_headers(request)
    
    response = requests.get(f"{API_RECETAS}{id}/", headers=headers)
    if response.status_code != 200:
        return redirect('ver_recetas')
    
    receta = response.json()

    if request.method == "POST":
        requests.delete(f"{API_RECETAS}{id}/", headers=headers)
        messages.success(request, "Receta eliminada")
        return redirect("ver_recetas")
    
    return render(request, "borrar_receta.html", {"receta": receta})

def eliminar_receta(request, id):
    response = requests.delete(f"{API_RECETAS}{id}/")

    if response.status_code == 204:
        messages.success(request, "Receta eliminada correctamente")
    else:
        messages.error(request, "No se pudo eliminar la receta")

    return redirect("ver_recetas")


def ver_recetas(request):
    if not request.session.get('token'):
        return redirect('login')

    user_id = request.session.get('user_id')
    headers = get_auth_headers(request)
    
    response = requests.get(API_RECETAS, headers=headers)
    if response.status_code != 200:
        messages.error(request, "Error al cargar las recetas")
        return render(request, "ver_recetas.html", {"recetas_data": []})

    all_recetas = response.json()
    
    mis_recetas = [r for r in all_recetas if r.get('usuario') == user_id]
    
    if not mis_recetas:
        return render(request, "ver_recetas.html", {"recetas_data": []})

    try:
        resp_rels = requests.get(API_RECETA_INGREDIENTE, headers=headers)
        all_rels = resp_rels.json() if resp_rels.status_code == 200 else []
        
        resp_ings = requests.get(API_INGREDIENTES, headers=headers)
        all_ings = resp_ings.json() if resp_ings.status_code == 200 else []
        
        ing_map = {i['id']: i for i in all_ings}
        
    except Exception as e:
        print(f"Error fetching details: {e}")
        all_rels = []
        ing_map = {}

    recetas_data = []
    
    for receta in mis_recetas:
        rels = [r for r in all_rels if r['receta'] == receta['id']]
        
        total_precio = 0
        for rel in rels:
            ing_id = rel['ingrediente']
            cantidad = rel['cantidad']
            ing_obj = ing_map.get(ing_id)
            
            if ing_obj:
                precio_unitario = ing_obj.get('costo_unitario', 0)
                total_precio += (precio_unitario * cantidad)
        
        recetas_data.append({
            "receta": receta,
            "precio": round(total_precio, 2) if total_precio > 0 else "No calculado"
        })

    return render(
        request,
        "ver_recetas.html",
        {"recetas_data": recetas_data}
    )

def ver_recetas_alumnos(request):
    resp_recetas = requests.get(API_RECETAS)
    recetas = resp_recetas.json() if resp_recetas.status_code == 200 else []
    
    resp_users = requests.get(API_ALUMNOS)
    usuarios = resp_users.json() if resp_users.status_code == 200 else []
    
    alumnos_ids = [
        u['id'] for u in usuarios 
        if u.get('nombre_rol') and 'alumno' in u['nombre_rol'].lower()
    ]
    
    recetas_alumnos_raw = [r for r in recetas if r['usuario'] in alumnos_ids]
    
    buscar = request.GET.get('buscar', '').lower()
    categoria_filtro = request.GET.get('categoria')
    letra = request.GET.get('letra')
    
    filtered_recetas = []
    for r in recetas_alumnos_raw:
        if buscar and buscar not in r['nombre'].lower():
            continue
        if categoria_filtro and r['categoria'] != categoria_filtro:
            continue
        if letra and not r['nombre'].upper().startswith(letra):
            continue
        filtered_recetas.append(r)
        
    if filtered_recetas:
        resp_rel = requests.get(API_RECETA_INGREDIENTE)
        all_rels = resp_rel.json() if resp_rel.status_code == 200 else []
        
        resp_ing = requests.get(API_INGREDIENTES)
        all_ings = resp_ing.json() if resp_ing.status_code == 200 else []
        ing_dict = {i['id']: i for i in all_ings}
        
        user_dict = {u['id']: u.get('username', 'Desconocido') for u in usuarios}
    else:
        all_rels = []
        ing_dict = {}
        user_dict = {}

    recetas_data = []
    all_categories = set()
    
    for r in recetas:
        if r.get('categoria'):
            all_categories.add(r['categoria'])
        
    for r in filtered_recetas:
        rels = [rel for rel in all_rels if rel['receta'] == r['id']]
        precio = 0
        for rel in rels:
            ing = ing_dict.get(rel['ingrediente'])
            if ing:
                precio += rel['cantidad'] * ing['costo_unitario']
        
        recetas_data.append({
            'receta': r,
            'precio': precio if precio > 0 else "No calculado",
            'usuario': user_dict.get(r['usuario'], 'Desconocido')
        })
        
    return render(request, "ver_recetas_alumnos.html", {
        "recetas_data": recetas_data,
        "categorias": sorted(list(all_categories))
    })
