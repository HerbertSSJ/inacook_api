import React, { useEffect, useState } from 'react';
import { API_BASE_URL } from '../api/config';

export default function EliminarIngrediente(){
  const [ingredientes, setIngredientes] = useState([]);
  const [error, setError] = useState(null);

  useEffect(()=>{ fetch(`${API_BASE_URL}/api/ingredientes/`).then(r=>r.ok?r.json():[]).then(setIngredientes).catch(e=>setError(e.message)); },[]);

  async function eliminar(id){
    if(!window.confirm('¿Eliminar ingrediente?')) return;
    try{ const token = localStorage.getItem('token'); const res = await fetch(`${API_BASE_URL}/api/ingredientes/${id}/`, { method:'DELETE', headers: { 'Authorization': token?`Token ${token}`:'' } }); if(!res.ok) throw new Error('Error'); setIngredientes(i=>i.filter(x=>x.id!==id)); }catch(err){ setError(err.message); }
  }

  return (
    <div className="page eliminar-ingrediente">
      <h1>Eliminar ingrediente</h1>
      <div className="container">
        {error && <div className="alert danger">{error}</div>}
        <ul>
          {ingredientes.map(i=> (
            <li key={i.id}>{i.nombre} <button className="btn btn-secondary" onClick={()=>eliminar(i.id)}>Eliminar</button></li>
          ))}
        </ul>
      </div>
    </div>
  );
}
