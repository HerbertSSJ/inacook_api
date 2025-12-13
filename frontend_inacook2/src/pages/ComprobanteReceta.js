import React, { useState, useEffect } from 'react';
import { API_BASE_URL } from '../api/config';
import { useParams } from 'react-router-dom';

export default function ComprobanteReceta(){
  const params = useParams();
  const [id, setId] = useState(params.id || '');
  const [receta, setReceta] = useState(null);
  const [error, setError] = useState(null);

  useEffect(()=>{
    if(params.id){ load(params.id); }
  },[params.id]);

  async function load(loadId){
    try{ const res = await fetch(`${API_BASE_URL}/api/recetas/${loadId}/`); if(!res.ok) throw new Error('No encontrada'); const d = await res.json(); setReceta(d); }catch(err){ setError(err.message); }
  }

  async function handleLoad(e){ e.preventDefault(); if(!id) return; await load(id); }

  return (
    <div className="page comprobante-receta">
      <h1>Comprobante de receta</h1>
      <div className="container">
        <form onSubmit={handleLoad} className="formulario">
          <label>ID receta<input value={id} onChange={e=>setId(e.target.value)} /></label>
          <button className="btn" type="submit">Cargar comprobante</button>
        </form>
        {error && <div className="alert danger">{error}</div>}
        {receta && (
          <div className="container">
            <h2>{receta.nombre || receta.titulo}</h2>
            <p>{receta.descripcion}</p>
            <p>Autor: {receta.autor || receta.owner}</p>
          </div>
        )}
      </div>
    </div>
  );
}
