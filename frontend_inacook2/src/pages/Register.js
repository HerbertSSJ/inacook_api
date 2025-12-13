import React, { useState } from 'react';
import { API_BASE_URL } from '../api/config';
import { useNavigate } from 'react-router-dom';

export default function Register(){
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [msg, setMsg] = useState(null);
  const navigate = useNavigate();

  async function handleSubmit(e){
    e.preventDefault();
    try{
      const res = await fetch(`${API_BASE_URL}/api/usuarios/`, {
        method: 'POST', headers: { 'Content-Type':'application/json' },
        body: JSON.stringify({ username: name, email, password })
      });
      if(!res.ok){
        let errText = 'Error al registrar';
        try{ const j = await res.json(); errText = j.error || JSON.stringify(j); }catch(_){ errText = await res.text(); }
        throw new Error(errText);
      }
      setMsg('Registro completado');
      window.setTimeout(()=> navigate('/login'), 900);
    }catch(err){ setMsg(err.message); }
  }

  return (
    <div className="page register">
      <h1>Registro</h1>
      <div className="container">
        {msg && <div className="alert info">{msg}</div>}
        <form onSubmit={handleSubmit} className="formulario">
          <label>Nombre<input name="name" value={name} onChange={e=>setName(e.target.value)} /></label>
          <label>Email<input name="email" value={email} onChange={e=>setEmail(e.target.value)} /></label>
          <label>Contraseña<input type="password" name="password" value={password} onChange={e=>setPassword(e.target.value)} /></label>
          <button className="btn" type="submit">Registrar</button>
        </form>
      </div>
    </div>
  );
}
