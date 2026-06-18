async function carregarProjetos () {
    const token = localStorage.getItem('token')
    if (!token) {window.location.href = 'index.html'}
    const response = await fetch('https://special-goldfish-jjpw4p7w599vc5gqg-5000.app.github.dev/projetos' , { headers: { 'Authorization': 'Bearer ' + token }})
    const data = await response.json()
    const grid = document.getElementById('projects-grid')
    data.projetos.forEach(projeto =>{
        grid.innerHTML += `
            <div class="project-card">
            <h3>${projeto.name}</h3>
            <p>${projeto.desc}</p>
        `
    })
}

carregarProjetos()