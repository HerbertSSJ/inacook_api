import React, { useEffect, useState } from 'react';
import { API_BASE_URL } from '../api/config';

export default function BorrarReceta(){
  const [recetas, setRecetas] = useState([]);
  const [error, setError] = useState(null);

  useEffect(()=>{
    fetch(`${API_BASE_URL}/api/recetas/`).then(r=>r.ok?r.json():[]).then(setRecetas).catch(e=>setError(e.message));
  },[]);

  async function borrar(id){
    if(!window.confirm('¿Eliminar receta?')) return;
    try{
      const token = localStorage.getItem('token');
      const res = await fetch(`${API_BASE_URL}/api/recetas/${id}/`, { method: 'DELETE', headers: { 'Authorization': token?`Token ${token}`:'' } });
      if(!res.ok) throw new Error('Error al borrar');
      setRecetas(r=>r.filter(x=>x.id!==id));
    }catch(err){ setError(err.message); }
  }

  return (
    <div className="page borrar-receta">
      <h1>Borrar receta</h1>
      <div className="container">
        {error && <div className="alert danger">{error}</div>}
        <table className="table-wide">
          <thead><tr><th>Título</th><th>Autor</th><th>Acciones</th></tr></thead>
          <tbody>
            {recetas.map(r=> (
              <tr key={r.id}>
                <td>{r.nombre || r.titulo || r.name}</td>
                <td>{r.autor || r.owner || r.user}</td>
                <td><button className="btn btn-secondary" onClick={()=>borrar(r.id)}>Borrar</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
