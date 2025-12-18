import requests
from django.shortcuts import render, redirect
from django.contrib import messages

API_RECETAS = "http://127.0.0.1:8000/api/recetas/"
API_COMPROBANTES = "http://127.0.0.1:8000/api/comprobantes/"
API_RECETA_INGREDIENTE = "http://127.0.0.1:8000/api/receta-ingrediente/"
API_INGREDIENTES = "http://127.0.0.1:8000/api/ingredientes/"
API_UNIDADES = "http://127.0.0.1:8000/api/unidades/"

def ver_comprobante(request, id):
    resp_r = requests.get(f"{API_RECETAS}{id}/")
    if resp_r.status_code != 200:
        messages.error(request, "Receta no encontrada")
        return redirect('ver_recetas')
    receta = resp_r.json()
    
    resp_c = requests.get(API_COMPROBANTES)
    comprobantes = resp_c.json() if resp_c.status_code == 200 else []
    
    comprobante = next((c for c in comprobantes if c.get('receta') == id), None)
    
    resp_rel = requests.get(API_RECETA_INGREDIENTE)
    all_rels = resp_rel.json() if resp_rel.status_code == 200 else []
    rels = [rel for rel in all_rels if rel['receta'] == id]
    
    resp_ing = requests.get(API_INGREDIENTES)
    ing_map = {i['id']: i for i in resp_ing.json()} if resp_ing.status_code == 200 else {}
    
    resp_uni = requests.get(API_UNIDADES) 
    uni_map = {u['id']: u['abreviatura'] for u in resp_uni.json()} if resp_uni.status_code == 200 else {}
    
    subtotal_sum = 0
    ingredientes_list = []
    
    for rel in rels:
        ing = ing_map.get(rel['ingrediente'])
        if ing:
            unidad_nombre = uni_map.get(ing.get('unidad_medicion'), '?')
            costo = ing['costo_unitario']
            cantidad = rel['cantidad']
            sub = costo * cantidad
            subtotal_sum += sub
            
            peso_total = None
            if isinstance(rel, dict):
                peso_total = rel.get('peso_total')
                if not peso_total:
                    peso_val = rel.get('peso')
                    try:
                        if peso_val is not None:
                            peso_total = float(peso_val) * float(cantidad)
                    except Exception:
                        peso_total = None

            ingredientes_list.append({
                'nombre': ing['nombre'],
                'cantidad': cantidad,
                'peso': rel.get('peso'),
                'peso_total': peso_total,
                'unidad': unidad_nombre,
                'precio': costo,
                'subtotal': sub
            })
            
    if comprobante:
        iva_rate = comprobante['iva']
        factor = comprobante['factor_multiplicacion']
    else:
        iva_rate = 19
        factor = 1
        
    iva_monto = subtotal_sum * (iva_rate / 100)
    total_final = (subtotal_sum + iva_monto) * factor
    
    return render(request, "comprobante_receta.html", {
        "receta": receta,
        "ingredientes": ingredientes_list,
        "comprobante": comprobante,
        "subtotal": subtotal_sum,
        "iva_monto": iva_monto,
        "total_final": total_final
    })
