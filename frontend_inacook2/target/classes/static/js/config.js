// Configuración del cliente frontend para conectarse a la API
// Por defecto asume que la API corre en http://localhost:8000
const API_BASE_URL = window.__API_BASE_URL__ || 'http://localhost:8000';

function getAuthToken(){
    return localStorage.getItem('inacook_token');
}

function setAuthToken(token){
    localStorage.setItem('inacook_token', token);
}

function clearAuthToken(){
    localStorage.removeItem('inacook_token');
}

function authHeader(){
    const t = getAuthToken();
    // DRF TokenAuth usa el prefijo 'Token '
    return t ? { 'Authorization': 'Token '+t } : {};
}
