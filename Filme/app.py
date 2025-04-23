from flask import Flask
from db import db
from route.filme_route import filme_route

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///filmes.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(filme_route)

if __name__ =='__main__':
    with app .app_context():
        db.create_all()

    app.run(debug=True)
