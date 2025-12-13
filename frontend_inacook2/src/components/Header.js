import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';

export default function Header(){
  const [token, setToken] = useState(null);
  const navigate = useNavigate();

  useEffect(()=>{ setToken(localStorage.getItem('token')); }, []);
  useEffect(()=>{
    function onAuth(){ setToken(localStorage.getItem('token')); }
    window.addEventListener('authChanged', onAuth);
    window.addEventListener('storage', onAuth);
    return ()=>{ window.removeEventListener('authChanged', onAuth); window.removeEventListener('storage', onAuth); }
  }, []);

  function logout(){ localStorage.removeItem('token'); setToken(null); navigate('/login'); }

  return (
    <header className="navbar">
      <div className="nav-container">
        <Link className="nav-logo" to="/">Inacook</Link>
        <ul className="nav-links">
            <li><Link to="/recetas">Mis Recetas</Link></li>
            <li><Link to="/subir">Subir Receta</Link></li>
            <li><Link to="/ingredientes">Ingredientes</Link></li>
            <li><Link to="/historial">Historial</Link></li>
            <li><Link to="/calculadora">Calculadora</Link></li>
            <li><Link to="/perfil">Perfil</Link></li>
          {token ? (
            <li><button className="btn btn-secondary" onClick={logout}>Cerrar Sesión</button></li>
          ) : (
            <li><Link to="/login">Login</Link></li>
          )}
        </ul>
      </div>
    </header>
  );
}
