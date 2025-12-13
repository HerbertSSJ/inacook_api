import { API_BASE_URL } from './config';
import { authHeader } from './auth';

export async function fetchRecetas(){
  const res = await fetch(`${API_BASE_URL}/api/recetas/`, { headers: { 'Content-Type':'application/json', ...authHeader() } });
  if(!res.ok) return [];
  return await res.json();
}
