from flask import Blueprint
from flask import request
from app.auth import token_obrigatorio
from flask import current_app
from app.database import db
from app.models import Project


projects_bp = Blueprint('projects', __name__)


@projects_bp.route('/projetos', methods=['POST'])
@token_obrigatorio
def criar_projetos(user_id):
    dados = request.get_json()
    name = dados.get('name')
    desc = dados.get('desc')
    if not name:
        return {"error": "nome é obrigatório"}, 400
    if not desc: 
        return {"error": "descrição é obrigatória"}, 400
    
    novo_projeto = Project(name=name, desc=desc, user_id=user_id)

    db.session.add(novo_projeto)
    db.session.commit() 

    return {"message": "Projeto Criado com sucesso!"}



@projects_bp.route('/projetos', methods=['GET'])
@token_obrigatorio
def listar_projetos (user_id):
    projects_list = []
    projetos = Project.query.filter_by(user_id=user_id).all()
    for projeto in projetos:
        projects_list.append ({
                "id" : projeto.id, 
                "name" : projeto.name,
                "desc" : projeto.desc,
                "created_at" : projeto.created_at,

        })
    return {"projetos" : projects_list}