export function authHeader(){
  const token = localStorage.getItem('token');
  return token ? { 'Authorization': `Token ${token}` } : {};
}
