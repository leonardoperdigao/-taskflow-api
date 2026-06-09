from flask import request
from app.database import db
from app.models import User
from app import app  

@app.route('/users', methods=['POST'])
def create_user():
    pass