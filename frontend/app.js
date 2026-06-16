document.getElementById('btn-login').addEventListener('click', async () => {
    const email = document.getElementById('email').value
    const senha = document.getElementById('senha').value
    
    const response = await fetch('https://special-goldfish-jjpw4p7w599vc5gqg-5000.app.github.dev/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: email, password: senha })
    })
    
    const data = await response.json()
    
    if (data.token) {
        localStorage.setItem('token', data.token)  
        window.location.href = 'dashboard.html'
    } else {
        alert('Email ou senha incorretos!')
    }
})