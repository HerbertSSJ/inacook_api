import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { API_BASE_URL } from '../api/config';
import { useNavigate } from 'react-router-dom';

export default function Login(){
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [msg, setMsg] = useState(null);
  const token = localStorage.getItem('token');

  const navigate = useNavigate();
  async function handleSubmit(e){
    e.preventDefault();
    try{
      const res = await fetch(`${API_BASE_URL}/api/token-auth/`, {
        method: 'POST', headers: { 'Content-Type':'application/json' },
        body: JSON.stringify({ username, password })
      });
      if(!res.ok) throw new Error('Credenciales inválidas');
      const data = await res.json();
      if(data.token){ localStorage.setItem('token', data.token); setMsg('Login correcto'); }
      if(data.token){
        window.dispatchEvent(new Event('authChanged'));
        navigate('/');
      }
    }catch(err){ setMsg(err.message); }
  }

  return (
    <div className="page login">
      <h1>Iniciar sesión</h1>
      <div className="container">
        {!token && <div className="alert success" style={{marginBottom:20}}>Sesión cerrada</div>}
        {msg && <div className="alert info">{msg}</div>}
        <form onSubmit={handleSubmit} className="formulario">
          <div className="form-row">
            <label><span>Nombre de usuario:</span><input name="username" value={username} onChange={e=>setUsername(e.target.value)} /></label>
          </div>
          <div className="form-row">
            <label><span>Contraseña:</span><input type="password" name="password" value={password} onChange={e=>setPassword(e.target.value)} /></label>
          </div>
          <div className="form-row">
            <button className="btn wide" type="submit">Iniciar sesión</button>
          </div>
          <div style={{marginTop:8}}>¿No tienes cuenta? <Link to="/register">Regístrate aquí</Link></div>
        </form>
      </div>
    </div>
  );
}
