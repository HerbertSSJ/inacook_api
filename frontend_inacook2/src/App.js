import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import VerRecetas from './pages/VerRecetas';
import SubirReceta from './pages/SubirReceta';
import Perfil from './pages/Perfil';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import Calculadora from './pages/Calculadora';
import CambiarContrasena from './pages/CambiarContrasena';
import ComprobanteReceta from './pages/ComprobanteReceta';
import CrearIngrediente from './pages/CrearIngrediente';
import EditarIngrediente from './pages/EditarIngrediente';
import EditarReceta from './pages/EditarReceta';
import EliminarIngrediente from './pages/EliminarIngrediente';
import VerHistorial from './pages/VerHistorial';
import VerIngredientes from './pages/VerIngredientes';
import VerRecetasAlumnos from './pages/VerRecetasAlumnos';
import BorrarReceta from './pages/BorrarReceta';

export default function App(){
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<ProtectedRoute><Dashboard/></ProtectedRoute>} />
        <Route path="/login" element={<Login/>} />
        <Route path="/register" element={<Register/>} />
        <Route path="/recetas" element={<ProtectedRoute><VerRecetas/></ProtectedRoute>} />
        <Route path="/recetas/:id" element={<ProtectedRoute><ComprobanteReceta/></ProtectedRoute>} />
        <Route path="/subir" element={<ProtectedRoute><SubirReceta/></ProtectedRoute>} />
        <Route path="/perfil" element={<ProtectedRoute><Perfil/></ProtectedRoute>} />
        <Route path="/calculadora" element={<ProtectedRoute><Calculadora/></ProtectedRoute>} />
        <Route path="/cambiar-contrasena" element={<ProtectedRoute><CambiarContrasena/></ProtectedRoute>} />
        <Route path="/comprobante" element={<ProtectedRoute><ComprobanteReceta/></ProtectedRoute>} />
        <Route path="/crear-ingrediente" element={<ProtectedRoute><CrearIngrediente/></ProtectedRoute>} />
        <Route path="/editar-ingrediente" element={<ProtectedRoute><EditarIngrediente/></ProtectedRoute>} />
        <Route path="/editar-receta" element={<ProtectedRoute><EditarReceta/></ProtectedRoute>} />
        <Route path="/eliminar-ingrediente" element={<ProtectedRoute><EliminarIngrediente/></ProtectedRoute>} />
        <Route path="/historial" element={<ProtectedRoute><VerHistorial/></ProtectedRoute>} />
        <Route path="/ingredientes" element={<ProtectedRoute><VerIngredientes/></ProtectedRoute>} />
        <Route path="/recetas-alumnos" element={<ProtectedRoute><VerRecetasAlumnos/></ProtectedRoute>} />
        <Route path="/borrar-receta" element={<ProtectedRoute><BorrarReceta/></ProtectedRoute>} />
      </Routes>
    </Layout>
  );
}
