document.getElementById('btn-cadastrar').addEventListener('click', async () => {
    const username = document.getElementById('username').value
    const email = document.getElementById('email').value
    const password = document.getElementById('password').value

    const response = await fetch('http://localhost:5000/users', {    
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password })
    })
    const data = await response.json()
    if (response.ok) {
        alert('Cadastro realizado com sucesso!')
        window.location.href = 'index.html'
    } else {
        alert(data.error)
    }       
})