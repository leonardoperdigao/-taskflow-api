from flask import request
from app.database import db
from app.models import User
from flask import Blueprint

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['POST'])
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



@users_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    usuario = User.query.get(id)
    if not usuario: 
        return {"error": "ID do usúario não encontrado ou não cadastrado."}, 404
    else:
        return {
            "id" : usuario.id,
            "username" : usuario.username,
            "email" : usuario.email
        }
        

@users_bp.route('/users/<int:id>', methods=['PUT'])
def get_atualizar(id):
    usuario = User.query.get(id) 
    if not usuario: 
        return {"error": "ID do usúario não encontrado ou não cadastrado."}, 404
    dados = request.get_json()
    username = dados.get('username')
    if username:
        usuario.username = username
    email = dados.get('email')
    if email:
        usuario.email = email
    
    db.session.commit()
    return {"message": "Alteração concluida com êxito!"}

@users_bp.route('/users/<int:id>', methods=['DELETE'])
def get_deletar(id):
    usuario = User.query.get(id)
    if not usuario: 
        return {"error": "Usúario não encontrado ou não cadastrado."}, 404
    db.session.delete(usuario)
    db.session.commit()
    return {"message": "Usuário removido com sucesso!"}