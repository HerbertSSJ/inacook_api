import React, { useState } from 'react';
import { API_BASE_URL } from '../api/config';

export default function EditarIngrediente(){
  const [id, setId] = useState('');
  const [nombre, setNombre] = useState('');
  const [msg, setMsg] = useState(null);

  async function handleLoad(e){ e.preventDefault(); if(!id) return; try{ const res = await fetch(`${API_BASE_URL}/api/ingredientes/${id}/`); if(!res.ok) throw new Error('No encontrado'); const d=await res.json(); setNombre(d.nombre||''); }catch(err){ setMsg(err.message); } }
  async function handleSave(e){ e.preventDefault(); try{ const token=localStorage.getItem('token'); const res = await fetch(`${API_BASE_URL}/api/ingredientes/${id}/`, { method:'PATCH', headers:{ 'Content-Type':'application/json','Authorization': token?`Token ${token}`:'' }, body: JSON.stringify({ nombre }) }); if(!res.ok) throw new Error('Error'); setMsg('Guardado'); }catch(err){ setMsg(err.message);} }

  return (
    <div className="page editar-ingrediente">
      <h1>Editar ingrediente</h1>
      <div className="container">
        {msg && <div className="alert info">{msg}</div>}
        <form onSubmit={handleLoad} className="formulario">
          <label>ID ingrediente<input value={id} onChange={e=>setId(e.target.value)} /></label>
          <button className="btn" type="submit">Cargar</button>
        </form>
        <form onSubmit={handleSave} className="formulario">
          <label>Nombre<input value={nombre} onChange={e=>setNombre(e.target.value)} /></label>
          <button className="btn" type="submit">Guardar</button>
        </form>
      </div>
    </div>
  );
}
