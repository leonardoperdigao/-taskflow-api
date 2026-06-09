from flask import request
from app.database import db
from app.models import User
from app import app  

@app.route('/users', methods=['POST'])
def create_user():
    dados = request.get_json()

    username = dados.get('username')
    if not username:
        return {"error": "username é obrigatório" }, 400
    
    email = dados.get('email')
    if not email:
        return {"error": "email é obrigatório" }, 400
    usuario_existente = User.query.filter_by(email=email).first()
    if usuario_existente:
        return {"error": "Email já cadastrado"}, 400
    

    password = dados.get('password')
    if not password:
        return {"error": "senha é obrigatória" }, 400
    

    novo_usuario = User(username=username, email=email, password=password)

    db.session.add(novo_usuario)
    db.session.commit()

    return {"message": "Usuário criado com sucesso!", "id": novo_usuario.id}, 201