import React, { useEffect, useState } from 'react';
import { fetchRecetas } from '../api/recipes';

export default function VerRecetas(){
  const [recetas, setRecetas] = useState([]);
  useEffect(()=>{
    fetchRecetas().then(r=>setRecetas(r)).catch(()=>{});
  },[]);
  return (
    <div className="page recetas">
      <h1>Recetas</h1>
      <div className="tabla-recetas container-wide">
        <table className="table-wide">
          <thead>
            <tr><th>Imagen</th><th>Título</th><th>Autor</th><th>Acciones</th></tr>
          </thead>
          <tbody>
            {recetas.map(r=> (
              <tr key={r.id}>
                <td>{r.imagen ? <img className="table-img" src={r.imagen} alt=""/> : <span className="no-image">Sin imagen</span>}</td>
                <td>{r.nombre || r.titulo || r.name}</td>
                <td>{r.autor || r.owner || r.user}</td>
                <td className="table-actions"><a className="btn btn-secondary" href={`#/recetas/${r.id}`}>Ver</a></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
