// Auth helpers: login, logout, check
async function loginUser(username, password){
    const url = `${API_BASE_URL}/token-auth/`;
    const resp = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    if(!resp.ok) throw new Error('Credenciales inválidas');
    const data = await resp.json();
    // DRF token endpoint devuelve { "token": "..." }
    if(data.token){
        setAuthToken(data.token);
        return data;
    }
    throw new Error('Respuesta inesperada del servidor');
}

function logoutUser(){
    clearAuthToken();
    window.location = '/login';
}

function isLoggedIn(){
    return !!getAuthToken();
}

// Attach logout button if present
document.addEventListener('DOMContentLoaded', ()=>{
    const logoutBtn = document.getElementById('logout-btn');
    if(logoutBtn){
        logoutBtn.addEventListener('click', e=>{ e.preventDefault(); logoutUser(); });
    }
});
