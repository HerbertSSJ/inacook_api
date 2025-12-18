import requests
from django.shortcuts import render, redirect
from django.contrib import messages

API_RECETAS = "http://127.0.0.1:8000/api/recetas/"
API_ALUMNOS = "http://127.0.0.1:8000/api/usuarios/"
API_RECETA_INGREDIENTE = "http://127.0.0.1:8000/api/receta-ingrediente/"
API_INGREDIENTES = "http://127.0.0.1:8000/api/ingredientes/"
API_UNIDADES = "http://127.0.0.1:8000/api/unidades/"
API_COMPROBANTES = "http://127.0.0.1:8000/api/comprobantes/"

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

    if not unidades:
        unidades = [
            {"nombre": "Gramo", "abreviatura": "g"},
            {"nombre": "Kilogramo", "abreviatura": "kg"},
            {"nombre": "Miligramo", "abreviatura": "mg"},
            {"nombre": "Litro", "abreviatura": "L"},
            {"nombre": "Mililitro", "abreviatura": "ml"},
            {"nombre": "Unidad", "abreviatura": "u"},
            {"nombre": "Cucharada", "abreviatura": "cda"},
            {"nombre": "Cucharadita", "abreviatura": "cdta"},
            {"nombre": "Taza", "abreviatura": "taza"},
        ]

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
                        
                        price_map = {int(i['id']): float(i.get('costo_unitario', 0)) for i in ingredientes}
                        subtotal = 0
                        for item in lista_ing:
                            ing_id = int(item['id'])
                            cantidad = float(item['cantidad'])
                            ing_data = {
                                "receta": receta_id,
                                "ingrediente": ing_id,
                                "cantidad": cantidad
                            }
                            # opcional: peso y peso_total enviados desde frontend
                            if item.get('peso') is not None:
                                try:
                                    ing_data['peso'] = float(item.get('peso'))
                                except Exception:
                                    pass
                            if item.get('peso_total') is not None:
                                try:
                                    ing_data['peso_total'] = float(item.get('peso_total'))
                                except Exception:
                                    pass
                            requests.post(API_RECETA_INGREDIENTE, json=ing_data, headers=headers)
                            subtotal += price_map.get(ing_id, 0) * cantidad

                
                        try:
                            comprobante_payload = {
                                "receta": receta_id,
                                "factor_multiplicacion": 1,
                                "iva": 19,
                                "precio_bruto": int(subtotal)
                            }
                            requests.post(API_COMPROBANTES, json=comprobante_payload, headers=headers)
                        except Exception as e:
                            print(f"Error creando comprobante: {e}")
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

    if not unidades_list:
        unidades_list = [
            {"nombre": "Gramo", "abreviatura": "g", "id": None},
            {"nombre": "Kilogramo", "abreviatura": "kg", "id": None},
            {"nombre": "Miligramo", "abreviatura": "mg", "id": None},
            {"nombre": "Litro", "abreviatura": "L", "id": None},
            {"nombre": "Mililitro", "abreviatura": "ml", "id": None},
            {"nombre": "Unidad", "abreviatura": "u", "id": None},
            {"nombre": "Cucharada", "abreviatura": "cda", "id": None},
            {"nombre": "Cucharadita", "abreviatura": "cdta", "id": None},
            {"nombre": "Taza", "abreviatura": "taza", "id": None},
        ]
    
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
                    'Ingrediente': ing_obj,
                    'Peso': rel.get('peso'),
                    'Peso_total': rel.get('peso_total')
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
                    
                    price_map = {int(i['id']): float(i.get('costo_unitario', 0)) for i in ingredientes_list}
                    subtotal = 0
                    for item in lista_ing:
                            ing_id = int(item['id'])
                            cantidad = float(item['cantidad'])
                            ing_data = {
                                "receta": id,
                                "ingrediente": ing_id,
                                "cantidad": cantidad
                            }
                            if item.get('peso') is not None:
                                try:
                                    ing_data['peso'] = float(item.get('peso'))
                                except Exception:
                                    pass
                            if item.get('peso_total') is not None:
                                try:
                                    ing_data['peso_total'] = float(item.get('peso_total'))
                                except Exception:
                                    pass
                            requests.post(API_RECETA_INGREDIENTE, json=ing_data, headers=headers)
                            subtotal += price_map.get(ing_id, 0) * cantidad

                    
                    try:
                        resp_c = requests.get(API_COMPROBANTES, headers=headers)
                        comprobantes = resp_c.json() if resp_c.status_code == 200 else []
                        existing = next((c for c in comprobantes if c.get('receta') == id), None)
                        payload = {
                            "receta": id,
                            "factor_multiplicacion": 1,
                            "iva": 19,
                            "precio_bruto": int(subtotal)
                        }
                        if existing:
                            
                            try:
                                requests.put(f"{API_COMPROBANTES}{existing['id']}/", json=payload, headers=headers)
                            except Exception:
                                pass
                        else:
                            try:
                                requests.post(API_COMPROBANTES, json=payload, headers=headers)
                            except Exception:
                                pass
                    except Exception:
                        pass

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
            "calidad": ing_obj['calidad'],
            "peso": ri.get('Peso'),
            "peso_total": ri.get('Peso_total')
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

    
    try:
        resp_rels = requests.get(API_RECETA_INGREDIENTE, headers=headers)
        all_rels = resp_rels.json() if resp_rels.status_code == 200 else []

        resp_ing = requests.get(API_INGREDIENTES, headers=headers)
        all_ings = resp_ing.json() if resp_ing.status_code == 200 else []
        ing_map = {i['id']: i for i in all_ings}

    
        resp_uni = requests.get(API_UNIDADES, headers=headers)
        uni_map = {u['id']: u for u in resp_uni.json()} if resp_uni.status_code == 200 else {}

        rels = [r for r in all_rels if r.get('receta') == id]

        ingredientes = []
        for r in rels:
            ing = ing_map.get(r.get('ingrediente'))
            if not ing:
                continue
            unidad_nombre = ''
            unidad_id = ing.get('unidad_medicion')
            if unidad_id:
                unidad = uni_map.get(unidad_id)
                unidad_nombre = unidad.get('abreviatura') if unidad else ''

            ingredientes.append({
                'nombre': ing.get('nombre'),
                'cantidad': r.get('cantidad'),
                'unidad': unidad_nombre,
                'precio': ing.get('costo_unitario')
            })
    except Exception:
        ingredientes = []

    if request.method == "POST":
        requests.delete(f"{API_RECETAS}{id}/", headers=headers)
        messages.success(request, "Receta eliminada")
        return redirect("ver_recetas")
    
    imagen = receta.get('imagen') if receta.get('imagen') else None
    return render(request, "borrar_receta.html", {"receta": receta, "imagen": imagen, "ingredientes": ingredientes})

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
    headers = get_auth_headers(request)
    resp_recetas = requests.get(API_RECETAS, headers=headers)
    recetas = resp_recetas.json() if resp_recetas.status_code == 200 else []

    resp_users = requests.get(API_ALUMNOS, headers=headers)
    usuarios = resp_users.json() if resp_users.status_code == 200 else []
    
    alumnos_ids = set()
    for u in usuarios:
        nombre_rol = (u.get('nombre_rol') or '').lower()
        
        if 'alumno' in nombre_rol or 'estudiante' in nombre_rol or u.get('rol') == 2:
            alumnos_ids.add(u.get('id'))
            if u.get('user'):
                alumnos_ids.add(u.get('user'))
    alumnos_ids = list(alumnos_ids)
    
    recetas_alumnos_raw = [r for r in recetas if r['usuario'] in alumnos_ids]
    
    buscar = request.GET.get('buscar', '').strip().lower()
    categoria_filtro = request.GET.get('categoria')
    if categoria_filtro:
        categoria_filtro = categoria_filtro.strip()
        if categoria_filtro.lower() == 'todas':
            categoria_filtro = None
        else:
            categoria_filtro = categoria_filtro.lower()

    letra = request.GET.get('letra')
    if letra:
        letra = letra.strip()
        if letra.lower() == 'todas':
            letra = None
        else:
            letra = letra.upper()
    
    filtered_recetas = []
    for r in recetas_alumnos_raw:
        
        if buscar and buscar not in r.get('nombre', '').lower():
            continue

        
        if categoria_filtro and (not r.get('categoria') or r.get('categoria', '').strip().lower() != categoria_filtro):
            continue

        
        if not buscar and letra and not r.get('nombre', '').upper().startswith(letra):
            continue

        filtered_recetas.append(r)
        
    if filtered_recetas:
        resp_rel = requests.get(API_RECETA_INGREDIENTE, headers=headers)
        all_rels = resp_rel.json() if resp_rel.status_code == 200 else []
        
        resp_ing = requests.get(API_INGREDIENTES, headers=headers)
        all_ings = resp_ing.json() if resp_ing.status_code == 200 else []
        ing_dict = {i['id']: i for i in all_ings}
        
        user_dict = {u['id']: u.get('username', 'Desconocido') for u in usuarios}
    else:
        all_rels = []
        ing_dict = {}
        user_dict = {}


    resp_comp = requests.get(API_COMPROBANTES, headers=headers)
    comprobantes = resp_comp.json() if resp_comp.status_code == 200 else []
    comp_map = {c.get('receta'): c for c in comprobantes}

    recetas_data = []
    all_categories = set()
    
    for r in recetas:
        if r.get('categoria'):
            all_categories.add(r['categoria'])
        
    for r in filtered_recetas:
        rels = [rel for rel in all_rels if rel['receta'] == r['id']]
        subtotal = 0
        for rel in rels:
            ing = ing_dict.get(rel['ingrediente'])
            if ing:
                subtotal += rel['cantidad'] * ing.get('costo_unitario', 0)

        
        comp = comp_map.get(r['id'])
        if comp:
            iva_rate = comp.get('iva', 19)
            factor = comp.get('factor_multiplicacion', 1)
        else:
            iva_rate = 19
            factor = 1

        iva_amount = subtotal * (iva_rate / 100)
        total_con_iva = round((subtotal + iva_amount) * factor, 2) if subtotal > 0 else "No calculado"

        
        nombre = r.get('nombre') or r.get('Nombre_Receta') or ''
        categoria = r.get('categoria') or r.get('Categoria') or ''
        tiempo = r.get('tiempo_preparacion') or r.get('Tiempo_Preparacion') or ''

        recetas_data.append({
            'id': r.get('id'),
            'nombre': nombre,
            'categoria': categoria,
            'tiempo': tiempo,
            'precio_subtotal': round(subtotal, 2) if subtotal > 0 else "No calculado",
            'precio_total': total_con_iva,
            'usuario': user_dict.get(r['usuario'], 'Desconocido')
        })
        
    return render(request, "ver_recetas_alumnos.html", {
        "recetas_data": recetas_data,
        "categorias": sorted(list(all_categories))
    })
