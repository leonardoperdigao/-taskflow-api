from flask import Flask, jsonify
from app.database import db
from app.models import User
from app.routes import users_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskflow.db'
db.init_app(app)
app.register_blueprint(users_bp)

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


