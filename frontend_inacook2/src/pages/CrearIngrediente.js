import React, { useState } from 'react';
import { API_BASE_URL } from '../api/config';
export default function CrearIngrediente(){
  const [nombre, setNombre] = useState('');
  const [msg, setMsg] = useState(null);
  async function handle(e){ e.preventDefault(); try{ const token=localStorage.getItem('token'); const res = await fetch(`${API_BASE_URL}/api/ingredientes/`, { method:'POST', headers:{ 'Content-Type':'application/json','Authorization':token?`Token ${token}`:'' }, body: JSON.stringify({ nombre }) }); if(!res.ok) throw new Error('Error'); setMsg('Ingrediente creado'); }catch(err){ setMsg(err.message);} }
  return (
    <div className="page crear-ingrediente">
      <h1>Crear ingrediente</h1>
      <div className="container">
        {msg && <div className="alert info">{msg}</div>}
        <form onSubmit={handle} className="formulario">
          <label>Nombre<input value={nombre} onChange={e=>setNombre(e.target.value)} /></label>
          <button className="btn" type="submit">Crear</button>
        </form>
      </div>
    </div>
  );
}
