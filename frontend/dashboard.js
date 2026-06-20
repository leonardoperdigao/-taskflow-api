let projetos = []

async function carregarProjetos () {
    const token = localStorage.getItem('token')
    if (!token) {window.location.href = 'index.html'}
    const response = await fetch('http://localhost:5000/projetos' , { headers: { 'Authorization': 'Bearer ' + token }})
    const data = await response.json()
    projetos = data.projetos
    const grid = document.getElementById('projects-grid')
    grid.innerHTML = '' 
    data.projetos.forEach(projeto =>{
        grid.innerHTML += `
            <div class="project-card">
            <h3>${projeto.name}</h3>
            <p>${projeto.desc}</p>
            <button class="btn-deletar" data-id="${projeto.id}">Deletar</button>
            </div>
        `
    })

    document.querySelectorAll('.btn-deletar').forEach( btn => {
    btn.addEventListener('click', async () => {
        const id = btn.dataset.id
        const token = localStorage.getItem('token')
        const del = await fetch(`http://localhost:5000/projetos/${id}`, {
        method: 'DELETE',   
        headers: { 'Authorization': 'Bearer ' + token }
    })
        carregarProjetos()
        })
    })
}

const modal = document.getElementById('modal')
const btnAdd = document.getElementById('btn-add')
const btnCancelar = document.getElementById('btn-cancelar')
const btnCriar = document.getElementById('btn-criar')

btnAdd.addEventListener('click', () => {
    modal.style.display = 'flex'
})

btnCancelar.addEventListener('click', () => {
    modal.style.display = 'none'
})

btnCriar.addEventListener('click', async () => {
    const proname = document.getElementById('nome-projeto').value
    const descname = document.getElementById('desc-projeto').value
    const token = localStorage.getItem('token')
    const existe = projetos.find(p => p.name === proname)
    if (existe) {
        alert('Já existe um projeto com esse nome!')
    return
}
    const response = await fetch('http://localhost:5000/projetos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer ' + token
        },
        body: JSON.stringify({ name: proname, desc: descname})
    })
modal.style.display = 'none'
carregarProjetos()
    const toast = document.getElementById('toast')
        toast.style.display = 'block'
        setTimeout(() => {
         toast.style.display = 'none'
        }, 3000)
})


carregarProjetos()


document.getElementById('btn-sair').addEventListener('click', () => {
    localStorage.removeItem('token')
    window.location.href = 'index.html'
})  