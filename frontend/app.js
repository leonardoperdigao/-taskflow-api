document.getElementById('btn-login').addEventListener('click', async () => {
    const email = document.getElementById('email').value
    const senha = document.getElementById('senha').value
    
    const response = await fetch('http://localhost:5000/login', {
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