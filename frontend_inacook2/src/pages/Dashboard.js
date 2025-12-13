import React from 'react';
import { Link } from 'react-router-dom';

export default function Dashboard(){
  return (
    <div className="page dashboard">
      <h1>Bienvenido,</h1>
      <div className="container">
        <p><strong>Rol:</strong></p>
        <p>Este es tu panel principal. Desde aquí puedes gestionar tus recetas, visualizar tu historial y acceder a las herramientas de la aplicación.</p>

        <div className="panel acciones-rapidas">
          <h2>Acciones rápidas</h2>
          <ul className="quick-actions">
            <li><Link className="btn big" to="/subir">Subir nueva receta</Link></li>
            <li><Link className="btn big" to="/recetas">Ver mis recetas</Link></li>
            <li><Link className="btn big" to="/calculadora">Calculadora</Link></li>
            <li><Link className="btn big" to="/historial">Historial</Link></li>
          </ul>
        </div>
      </div>
    </div>
  );
}
