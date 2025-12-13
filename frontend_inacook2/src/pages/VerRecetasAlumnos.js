import React, { useEffect, useState } from 'react';
import { API_BASE_URL } from '../api/config';

export default function VerRecetasAlumnos(){
  const [byOwner, setByOwner] = useState({});
  useEffect(()=>{
    fetch(`${API_BASE_URL}/api/recetas/`).then(r=>r.ok?r.json():[]).then(list=>{
      const grouped = {};
      list.forEach(r=>{ const owner = r.autor||r.owner||'Desconocido'; (grouped[owner] = grouped[owner]||[]).push(r); });
      setByOwner(grouped);
    }).catch(()=>{});
  },[]);

  return (
    <div className="page ver-recetas-alumnos">
      <h1>Recetas de alumnos</h1>
      <div className="container">
        {Object.keys(byOwner).map(owner=> (
          <div key={owner} className="container-wide">
            <h3>{owner}</h3>
            <ul>
              {byOwner[owner].map(r=> <li key={r.id}>{r.nombre||r.titulo}</li>)}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}
