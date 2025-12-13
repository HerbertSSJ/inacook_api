import React, { useState } from 'react';
import { API_BASE_URL } from '../api/config';
export default function CambiarContrasena(){
  const [oldp, setOldp] = useState('');
  const [newp, setNewp] = useState('');
  const [msg, setMsg] = useState(null);
  async function handle(e){
    e.preventDefault();
    try{
      const token = localStorage.getItem('token');
      const res = await fetch(`${API_BASE_URL}/change-password/`, { method:'POST', headers: { 'Content-Type':'application/json', 'Authorization': token?`Token ${token}`:'' }, body: JSON.stringify({ old_password: oldp, new_password: newp }) });
      if(!res.ok) throw new Error('Error al cambiar contraseña');
      setMsg('Contraseña cambiada');
    }catch(err){ setMsg(err.message); }
  }
  return (
    <div className="page cambiar-contrasena">
      <h1>Cambiar contraseña</h1>
      <div className="container">
        {msg && <div className="alert info">{msg}</div>}
        <form onSubmit={handle} className="formulario">
          <label>Contraseña actual<input type="password" value={oldp} onChange={e=>setOldp(e.target.value)} /></label>
          <label>Nueva contraseña<input type="password" value={newp} onChange={e=>setNewp(e.target.value)} /></label>
          <button className="btn" type="submit">Cambiar</button>
        </form>
      </div>
    </div>
  );
}
