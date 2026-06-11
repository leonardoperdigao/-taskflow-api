from flask import request
from app.database import db
from app.models import User
from flask import Blueprint
from werkzeug.security import generate_password_hash , check_password_hash
import jwt
from datetime import datetime, timedelta 
from flask import current_app
from app.auth import token_obrigatorio

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
    
    hash_senha = generate_password_hash(password)
    

    novo_usuario = User(username=username, email=email, password=hash_senha)

    db.session.add(novo_usuario)
    db.session.commit()

    return {"message": "Usuário criado com sucesso!", "id": novo_usuario.id}, 201



@users_bp.route('/users/<int:id>', methods=['GET'])
@token_obrigatorio
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
@token_obrigatorio
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
@token_obrigatorio
def get_deletar(id):
    usuario = User.query.get(id)
    if not usuario: 
        return {"error": "Usúario não encontrado ou não cadastrado."}, 404
    db.session.delete(usuario)
    db.session.commit()
    return {"message": "Usuário removido com sucesso!"}



@users_bp.route('/login', methods = ['POST'])
def get_login ():
    dados = request.get_json()
    email = dados.get('email') 
    password = dados.get('password')
    if not email:
        return {"erro": "email não encotrado."} , 404 
    if not password: 
        return {"erro": "senha não encotrada."} , 404 
    
    usuario = User.query.filter_by(email=email).first()

    if not usuario:
        return {"error": "usuário não encontrado"}, 404

    senha_correta = check_password_hash(usuario.password, password)
    if not senha_correta: 
        return {"message":"senha incorreta."}, 401
    

    token = jwt.encode(
        {
        "user_id": usuario.id,
        "exp" : datetime.utcnow() + timedelta(hours=2) 
        },
        current_app.config['SECRET_KEY'],   
        algorithm="HS256"       

    )

    return {"token" : token}, 200


