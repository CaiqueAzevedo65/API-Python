from db import db 

class Livro(db.Model):
    __tablename__ = 'livros'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(80), nullable=False)
    genero = db.Column(db.String(80), nullable=False)
    paginas = db.Column(db.Integer, nullable=False)
    ano_lancamento = db.Column(db.Integer, nullable=False)
    autor = db.Column(db.String(80), nullable=False)

    def json(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'genero': self.genero,
            'paginas': self.paginas,
            'ano_lancamento': self.ano_lancamento,
            'autor': self.autor
        }