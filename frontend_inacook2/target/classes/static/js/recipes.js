// Recipes CRUD using fetch and token auth
async function fetchRecipes(){
    const url = `${API_BASE_URL}/recetas/`;
    const resp = await fetch(url, { headers: { 'Content-Type':'application/json', ...authHeader() } });
    if(!resp.ok) throw new Error('Error al obtener recetas');
    return await resp.json();
}

function renderRecipes(list, container){
    container.innerHTML = '';
    if(!list || list.length===0){ container.innerHTML = '<p>No hay recetas.</p>'; return; }
    list.forEach(r=>{
        const card = document.createElement('div');
        card.className = 'receta-card';
        card.innerHTML = `
            <h3>${r.Nombre_Receta}</h3>
            <p><strong>Categoría:</strong> ${r.Categoria || ''}</p>
            <p><strong>Tiempo:</strong> ${r.Tiempo_Preparacion || ''}</p>
            <p>${r.Procedimiento ? r.Procedimiento.substring(0,200) : ''}</p>
            <div class="acciones-receta">
                <button class="btn" data-id="${r.id}">Ver</button>
                <button class="btn btn-secondary" data-edit-id="${r.id}">Editar</button>
                <button class="btn btn-danger" data-del-id="${r.id}">Borrar</button>
            </div>
        `;
        container.appendChild(card);
    });
}

async function deleteRecipe(id){
    if(!confirm('Confirmar eliminación')) return;
    const url = `${API_BASE_URL}/recetas/${id}/`;
    const resp = await fetch(url, { method: 'DELETE', headers: { ...authHeader() } });
    if(!resp.ok) throw new Error('Error al borrar');
    return true;
}

async function createRecipe(data){
    const url = `${API_BASE_URL}/recetas/`;
    const resp = await fetch(url, { method: 'POST', headers: { 'Content-Type':'application/json', ...authHeader() }, body: JSON.stringify(data) });
    if(!resp.ok) {
        const err = await resp.json().catch(()=>null);
        throw new Error(err?.detail || 'Error al crear');
    }
    return await resp.json();
}

async function updateRecipe(id, data){
    const url = `${API_BASE_URL}/recetas/${id}/`;
    const resp = await fetch(url, { method: 'PUT', headers: { 'Content-Type':'application/json', ...authHeader() }, body: JSON.stringify(data) });
    if(!resp.ok) throw new Error('Error al actualizar');
    return await resp.json();
}

// Helpers to attach events on ver_recetas page
document.addEventListener('DOMContentLoaded', async ()=>{
    const listContainer = document.getElementById('recetas-list');
    if(listContainer){
        try{
            const list = await fetchRecipes();
            renderRecipes(list, listContainer);

            // delegate delete/edit buttons
            listContainer.addEventListener('click', async (e)=>{
                const delId = e.target.dataset.delId;
                const editId = e.target.dataset.editId;
                const viewId = e.target.dataset.id;
                if(delId){ await deleteRecipe(delId); const newList = await fetchRecipes(); renderRecipes(newList, listContainer); }
                if(editId){ window.location = `/editar_receta?edit=${editId}`; }
                if(viewId){ window.location = `/comprobante_receta?receta=${viewId}`; }
            });
        }catch(err){ listContainer.innerHTML = `<p style="color:red">${err.message}</p>`; }
    }
});
