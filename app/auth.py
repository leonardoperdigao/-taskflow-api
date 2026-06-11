from functools import wraps
from flask import request, current_app
import jwt

def token_obrigatorio(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth:
            return{"error":"Token invalido ou inexistente."} , 401
        token = auth.split(' ') [1]
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return {"error":"Token inválido."}

        return f(*args, **kwargs, user_id=payload['user_id'])
    return wrapper


