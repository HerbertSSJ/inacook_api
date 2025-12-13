import React, { useEffect, useState } from 'react';
import { API_BASE_URL } from '../api/config';
export default function VerIngredientes(){
  const [ingredientes, setIngredientes] = useState([]);
  useEffect(()=>{ fetch(`${API_BASE_URL}/api/ingredientes/`).then(r=>r.ok?r.json():[]).then(setIngredientes).catch(()=>{}); },[]);
  return (
    <div className="page ver-ingredientes">
      <h1>Ingredientes</h1>
      <div className="container">
        <ul>
          {ingredientes.map(i=> <li key={i.id}>{i.nombre}</li>)}
        </ul>
      </div>
    </div>
  );
}
