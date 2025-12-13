import React, { useState } from 'react';
import { API_BASE_URL } from '../api/config';

export default function EditarReceta(){
  const [id, setId] = useState('');
  const [titulo, setTitulo] = useState('');
  const [descripcion, setDescripcion] = useState('');
  const [msg, setMsg] = useState(null);

  async function handleLoad(e){
    e.preventDefault();
    if(!id) return;
    try{ const res = await fetch(`${API_BASE_URL}/api/recetas/${id}/`); if(!res.ok) throw new Error('No encontrada'); const data = await res.json(); setTitulo(data.nombre||data.titulo||''); setDescripcion(data.descripcion||''); }catch(err){ setMsg(err.message); }
  }

  async function handleSave(e){
    e.preventDefault();
    try{ const token=localStorage.getItem('token'); const res = await fetch(`${API_BASE_URL}/api/recetas/${id}/`, { method:'PATCH', headers: { 'Content-Type':'application/json','Authorization': token?`Token ${token}`:'' }, body: JSON.stringify({ nombre: titulo, descripcion }) }); if(!res.ok) throw new Error('Error al guardar'); setMsg('Guardado'); }catch(err){ setMsg(err.message); }
  }

  return (
    <div className="page editar-receta">
      <h1>Editar receta</h1>
      <div className="container">
        {msg && <div className="alert info">{msg}</div>}
        <form onSubmit={handleLoad} className="formulario">
          <label>ID de receta<input value={id} onChange={e=>setId(e.target.value)} /></label>
          <button className="btn" type="submit">Cargar</button>
        </form>
        <form onSubmit={handleSave} className="formulario">
          <label>Título<input value={titulo} onChange={e=>setTitulo(e.target.value)} /></label>
          <label>Descripción<textarea value={descripcion} onChange={e=>setDescripcion(e.target.value)} /></label>
          <button className="btn" type="submit">Guardar</button>
        </form>
      </div>
    </div>
  );
}
