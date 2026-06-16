from flask import Flask, jsonify
from app.database import db
from app.models import User, Project, Task
from app.routes import users_bp
from dotenv import load_dotenv
from app.projects import projects_bp
from app.tasks import tasks_bp
from flask_cors import CORS
import os


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskflow.db'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
CORS(app, origins="*")
db.init_app(app)
app.register_blueprint(projects_bp)
app.register_blueprint(users_bp)
app.register_blueprint(tasks_bp)

with app.app_context():
    db.create_all()

@app.route('/')
def hello():
    return jsonify({'message': 'TaskFlow API rodando!'})
@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


