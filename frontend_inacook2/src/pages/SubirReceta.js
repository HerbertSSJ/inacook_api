import React, { useState } from 'react';
import { API_BASE_URL } from '../api/config';

export default function SubirReceta(){
  const [titulo, setTitulo] = useState('');
  const [descripcion, setDescripcion] = useState('');
  const [msg, setMsg] = useState(null);

  async function handleSubmit(e){
    e.preventDefault();
    try{
      const token = localStorage.getItem('token');
      const form = new FormData();
      form.append('titulo', titulo);
      form.append('descripcion', descripcion);
      const res = await fetch(`${API_BASE_URL}/api/recetas/`, { method: 'POST', headers: { 'Authorization': token ? `Token ${token}` : '' }, body: form });
      if(!res.ok) throw new Error('Error al subir receta');
      setMsg('Receta subida');
    }catch(err){ setMsg(err.message); }
  }

  return (
    <div className="page subir">
      <h1>Subir receta</h1>
      <div className="container">
        {msg && <div className="alert info">{msg}</div>}
        <form className="formulario" onSubmit={handleSubmit}>
          <label>Título<input value={titulo} onChange={e=>setTitulo(e.target.value)} /></label>
          <label>Descripción<textarea value={descripcion} onChange={e=>setDescripcion(e.target.value)} /></label>
          <label>Imagen<input type="file" name="imagen"/></label>
          <button className="btn" type="submit">Subir</button>
        </form>
      </div>
    </div>
  );
}
