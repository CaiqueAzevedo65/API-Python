from model.filme_model import Filme
from db import db
import json
from flask import make_response
from sqlalchemy import func


# GET
def get_filmes():
    filmes = Filme.query.all()
    response = make_response(
        json.dumps({
            'mensagem': 'Lista de filmes.',
            'dados': [filme.json() for filme in filmes]
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'
    return response

def get_filmes_id(id_filme):
    filme = Filme.query.get(id_filme)
    if filme:
        response = make_response(
            json.dumps({
                'mensagem': 'Filme encontrado.',
                'dado': filme.json()
            }, ensure_ascii=False, sort_keys=False)
        )
        response.headers['Content-Type'] = 'application/json'
        return response
    else: 
        response = make_response(
            json.dumps({
                'mensagem': 'Filme não encontrado ou cadastrado.',
                'dado': {}
            }, ensure_ascii=False, sort_keys=False)
        )
        response.headers['Content-Type'] = 'application/json'
        return response

def get_first_filme():
    filme = Filme.query.first()
    response = make_response(
        json.dumps({
            'mensagem': 'Filme encontrado.',
            'dado': filme.json()
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'
    return response

def get_filmes_filter_genero(genero):
    filmes = Filme.query.filter(Filme.genero == genero)
    response = make_response(
        json.dumps({
            'mensagem': f'Lista de filmes com o genero {genero}.',
            'dado': [filme.json() for filme in filmes]
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'
    return response

def get_filmes_filter_by_diretor(diretor):
    filmes = Filme.query.filter_by(diretor=diretor).all()
    response = make_response(
        json.dumps({
            'mensagem': f'Lista de filmes feitos por {diretor}.',
            'dado': [filme.json() for filme in filmes]
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'
    return response

def get_filmes_order_by_duracao():
    filmes = Filme.query.order_by(Filme.duracao).all()
    response = make_response(
        json.dumps({
            'mensagem': 'Lista de filmes ordenados por duração.',
            'dado': [filme.json() for filme in filmes]
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'
    return response

def get_filmes_limitados(limite=3):
    filmes = Filme.query.limit(limite).all()
    response = make_response(
        json.dumps({
            'mensagem': 'Lista parcial de filmes.',
            'dado': [filme.json() for filme in filmes]
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'
    return response

def get_filmes_offset(offset,limite=3):
    filmes = Filme.query.offset(offset).limit(limite).all()     # offset ignora os primeiros registros 
    response = make_response(
        json.dumps({
            'mensagem': 'Lista parcial de filmes.',
            'dado': [filme.json() for filme in filmes]
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'
    return response 

def contar_filmes():
    quant_filmes = Filme.query.count()
    return f'Total de filmes: {str(quant_filmes)}'

def buscar_filmes_paginados_1():
    filmes = Filme.query.paginate(per_page=3,page=1).items
    response = make_response(
        json.dumps({
            'mensagem': 'Filmes paginados.',
            'dado': [filme.json() for filme in filmes]
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'
    return response 

def buscar_generos_filmes_diferentes():
    generos = Filme.query.with_entities(Filme.genero).distinct().all()
    return f'Generos: {str(generos)}'

def contagem_generos_filmes(): 
    filmes = Filme.query.with_entities(Filme.genero, func.count(Filme.id)).group_by(Filme.genero).all()
    return f'Contagem de gêneros: {str(filmes)}'

def buscar_titulos_filmes():
    titulos = Filme.query.with_entities(Filme.titulo).all()
    return f'Títulos: {str(titulos)}'

def buscar_exist_filmes(titulo):
    existe = Filme.query.filter(Filme.titulo == titulo).exists()
    return f'O filme {titulo} {existe}'


# POST
def create_filme(filme_data):
    if not all(key in filme_data for key in ['titulo', 'genero', 'duracao', 'ano_lancamento', 'diretor']):
        response = make_response(
            json.dumps({'mensagem': 'título, gênero, duração, ano de lançamento e diretor são obrigatórios'}, ensure_ascii=False),
            400  
        )
        response.headers['Content-Type'] = 'application/json'
        return response
    

    novo_filme = Filme(
        titulo=filme_data['titulo'],
        genero=filme_data['genero'],
        duracao=filme_data['duracao'],
        ano_lancamento=filme_data['ano_lancamento'],
        diretor=filme_data['diretor']
    )

    db.session.add(novo_filme)
    db.session.commit()

    response = make_response(
        json.dumps({
            'mensagem': 'Filme cadastrado com sucesso.',
            'filme': novo_filme.json()
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'
    return response


# PUT
def update_filme(id_filme, filme_data):
    filme = Filme.query.get(id_filme)  # Busca o filme pelo ID

    if not filme:  # Se o filme não for encontrado, retorna erro
        response = make_response(
            json.dumps({'mensagem': 'Filme não encontrado.'}, ensure_ascii=False),
            404  # Código HTTP 404 para "Não encontrado"
        )
        response.headers['Content-Type'] = 'application/json'  # Garante que a resposta seja em JSON
        return response

    # Valida se todos os campos obrigatórios foram fornecidos
    if not all(key in filme_data for key in ['titulo', 'genero', 'duracao', 'ano_lancamento', 'diretor']):
        response = make_response(
            json.dumps({'mensagem': 'Dados inválidos. Título, gênero, duração, ano de lançamento e diretor são obrigatórios'}, ensure_ascii=False),
            400  # Código HTTP 400 para requisição inválida
        )
        response.headers['Content-Type'] = 'application/json'  # Define que a resposta é em JSON
        return response

    filme.titulo=filme_data['titulo']
    filme.genero=filme_data['genero']
    filme.duracao=filme_data['duracao']
    filme.ano_lancamento=filme_data['ano_lancamento']
    filme.diretor=filme_data['diretor']

    db.session.commit()  # Confirma a atualização no banco de dados

    # Retorna a resposta com os dados do filme atualizado
    response = make_response(
        json.dumps({
            'mensagem': 'Filme atualizado com sucesso.',
            'filme': filme.json()
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'  # Define que a resposta é em JSON
    return response

# DELETE
def delete_filme(filme_id):
    filme = Filme.query.get(filme_id)
    if not filme :
        response = make_response(
            json.dumps({'mensagem': 'Filme não encontrado.'}, ensure_ascii=False),
            400
        )
        response.headers['Content-Type'] = 'application/json'
        return response
    
    db.session.delete(filme)
    db.session.commit()

    response = make_response(
        json.dumps({'mensagem': 'Filme excluído com sucesso.'}, ensure_ascii=False, sort_keys=False)
        )
    response.headers['Content-Type'] = 'application/json'
    return response