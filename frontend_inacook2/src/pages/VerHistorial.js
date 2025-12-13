import React, { useEffect, useState } from 'react';
import { API_BASE_URL } from '../api/config';

export default function VerHistorial(){
  const [items, setItems] = useState([]);
  useEffect(()=>{ fetch(`${API_BASE_URL}/historial/`).then(r=>r.ok?r.json():[]).then(setItems).catch(()=>{}); },[]);
  return (
    <div className="page ver-historial">
      <h1>Historial</h1>
      <div className="container">
        <ul>
          {items.map((it, idx)=> <li key={idx}>{it.mensaje || JSON.stringify(it)}</li>)}
        </ul>
      </div>
    </div>
  );
}
