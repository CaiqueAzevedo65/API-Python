from flask import Flask
from flask_jwt_extended import JWTManager
from db import init_db
from user_route import user_bp

app = Flask(__name__)
app.config.from_pyfile('config.py')
jwt = JWTManager(app)
init_db()
app.register_blueprint(user_bp, url_prefix='/users')
if __name__ == '__main__':
    app.run(debug=True)