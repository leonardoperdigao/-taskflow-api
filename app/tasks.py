from flask import Blueprint
from flask import request
from app.auth import token_obrigatorio
from flask import current_app
from app.database import db
from app.models import Task 

tasks_bp = Blueprint('tasks', __name__)  

@tasks_bp.route('/tasks', methods=['POST'])
@token_obrigatorio
def criar_tasks(user_id):
    dados = request.get_json()
    title = dados.get('title')
    desc_task = dados.get('desc_task')
    status = dados.get('status')
    prioridade = dados.get ('prioridade')
    project_id = dados.get ('project_id')
    if not title:
        return {"error": "O titulo da tarefa e obrigatório."}, 400
    if not project_id: 
        return {"error": "O id do projeto é obrigatório."}, 400
    nova_tarefa = Task (title=title, desc_task=desc_task, status=status, prioridade=prioridade, project_id=project_id)
    
    db.session.add(nova_tarefa)
    db.session.commit() 

    return {"message": "Tarefa adicionada ao projeto com sucesso!"}
    

@tasks_bp.route('/projetos/<int:project_id>/tasks', methods=['GET'])
@token_obrigatorio
def listar_tasks(user_id, project_id):
     lista_tasks = []
     tasks = Task.query.filter_by(project_id=project_id).all()
     for task in tasks:
         lista_tasks.append ({
                "id" : task.id, 
                "title" : task.title,
                "desc" : task.desc_task,
                "created_at" : task.created_at,
                "prioridade" : task.prioridade,
                "status" : task.status,

        })
     return {"tasks": lista_tasks}


@tasks_bp.route('/tasks/<int:id>', methods=['GET'])
@token_obrigatorio
def buscar_task (user_id, id):
    tasks = Task.query.get(id)
    if not tasks:
        return {"error": "tarefa não encontrado ou não criada."}
    else: 
        return {
            "id" : tasks.id, 
            "title" : tasks.title,
            "desc" : tasks.desc_task,
            "created_at" : tasks.created_at,
            "prioridade" : tasks.prioridade,
            "status" : tasks.status,
    }


@tasks_bp.route('/tasks/<int:id>', methods=['PUT'])
@token_obrigatorio
def atualizar_task (user_id, id):
    dados = request.get_json()
    tasks = Task.query.get(id)
    if not tasks:
        return {"error": "tarefa não existe."}, 404
    title = dados.get('title')
    desc_task = dados.get('desc_task')
    if title:
        tasks.title = title
    if desc_task:
        tasks.desc_task = desc_task

    db.session.commit()
    return {"message": "Tarefa atualizada com sucesso!"}

@tasks_bp.route('/tasks/<int:id>', methods=['DELETE'])
@token_obrigatorio
def deletar_task (user_id, id):
    tasks = Task.query.get(id)
    if not tasks:
        return {"error": "tarefa não existe."}, 404
    db.session.delete(tasks)
    db.session.commit()
    return {"message": "Tarefa removido com sucesso!"}