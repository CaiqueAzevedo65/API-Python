from db import db 

class Filme(db.Model):
    __tablename__ = 'filmes'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(80), nullable=False)
    genero = db.Column(db.String(80), nullable=False)
    duracao = db.Column(db.Integer, nullable=False)
    ano_lancamento = db.Column(db.Integer, nullable=False)
    diretor = db.Column(db.String(80), nullable=False)

    def json(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'genero': self.genero,
            'duracao': self.duracao,
            'ano_lancamento': self.ano_lancamento,
            'diretor': self.diretor
        }