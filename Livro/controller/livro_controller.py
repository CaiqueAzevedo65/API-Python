from model.livro_model import Livro
from db import db
import json
from flask import make_response, request
from sqlalchemy import func


# GET
def get_livros():
    livros = Livro.query.all()
    response = make_response(
        json.dumps({
            'mensagem': 'Lista de livros.',
            'dados': [livro.json() for livro in livros]
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'
    return response

def get_livros_id(id_livro):
    livro = Livro.query.get(id_livro)
    if livro:
        response = make_response(
            json.dumps({
                'mensagem': 'Livro encontrado.',
                'dado': livro.json()
            }, ensure_ascii=False, sort_keys=False)
        )
        response.headers['Content-Type'] = 'application/json'
        return response
    else: 
        response = make_response(
            json.dumps({
                'mensagem': 'Livro não encontrado ou cadastrado.',
                'dado': {}
            }, ensure_ascii=False, sort_keys=False)
        )
        response.headers['Content-Type'] = 'application/json'
        return response

def get_first_livro():
    livro = Livro.query.first()
    response = make_response(
        json.dumps({
            'mensagem': 'Livro encontrado.',
            'dado': livro.json()
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'
    return response

def get_livros_filter_genero(genero):
    livros = Livro.query.filter(Livro.genero == genero)
    response = make_response(
        json.dumps({
            'mensagem': f'Lista de livros com o genero {genero}.',
            'dado': [livro.json() for livro in livros]
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'
    return response

def get_livros_filter_by_diretor(diretor):
    livros = Livro.query.filter_by(diretor=diretor).all()
    response = make_response(
        json.dumps({
            'mensagem': f'Lista de livros feitos por {diretor}.',
            'dado': [livro.json() for livro in livros]
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'
    return response

def get_livros_order_by_duracao():
    livros = Livro.query.order_by(Livro.duracao).all()
    response = make_response(
        json.dumps({
            'mensagem': 'Lista de livros ordenados por duração.',
            'dado': [livro.json() for livro in livros]
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'
    return response

def get_livros_limitados(limite=3):
    livros = Livro.query.limit(limite).all()
    response = make_response(
        json.dumps({
            'mensagem': 'Lista parcial de livros.',
            'dado': [livro.json() for livro in livros]
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'
    return response

def get_livros_offset(offset,limite=3):
    livros = Livro.query.offset(offset).limit(limite).all()     # offset ignora os primeiros registros 
    response = make_response(
        json.dumps({
            'mensagem': 'Lista parcial de livros.',
            'dado': [livro.json() for livro in livros]
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'
    return response 

def contar_livros():
    quant_livros = Livro.query.count()
    return f'Total de livros: {str(quant_livros)}'

def buscar_livros_paginados_1():
    livros = Livro.query.paginate(per_page=3,page=1).items
    response = make_response(
        json.dumps({
            'mensagem': 'Livros paginados.',
            'dado': [livro.json() for livro in livros]
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'
    return response 

def buscar_generos_livros_diferentes():
    generos = Livro.query.with_entities(Livro.genero).distinct().all()
    return f'Generos: {str(generos)}'

def contagem_generos_livros(): 
    livros = Livro.query.with_entities(Livro.genero, func.count(Livro.id)).group_by(Livro.genero).all()
    return f'Contagem de gêneros: {str(livros)}'

def buscar_titulos_livros():
    titulos = Livro.query.with_entities(Livro.titulo).all()
    return f'Títulos: {str(titulos)}'

def buscar_exist_livros(titulo):
    existe = Livro.query.filter(Livro.titulo == titulo).exists()
    return f'O livro {titulo} {existe}'


# POST
def create_livro(livro_data):
    if not all(key in livro_data for key in ['titulo', 'genero', 'paginas', 'ano_lancamento', 'autor']):
        response = make_response(
            json.dumps({'mensagem': 'título, gênero, número de páginas, ano de lançamento e autor são obrigatórios'}, ensure_ascii=False),
            400  
        )
        response.headers['Content-Type'] = 'application/json'
        return response
    

    # não aceitamos livros de Edgar Allan Poe

    if livro_data['autor'] == 'Edgar Allan Poe':
        return 'Não aceitamos obras desse autor. Melhore o seu gosto literário!'

    else:
        novo_livro = Livro(
            titulo=livro_data['titulo'],
            genero=livro_data['genero'],
            paginas=livro_data['paginas'],
            ano_lancamento=livro_data['ano_lancamento'],
            autor=livro_data['autor']
        )

        db.session.add(novo_livro)
        db.session.commit()

        response = make_response(
            json.dumps({
                'mensagem': 'Livro cadastrado com sucesso.',
                'livro': novo_livro.json()
            }, ensure_ascii=False, sort_keys=False)
        )
        response.headers['Content-Type'] = 'application/json'
        return response


# PUT
def update_livro(id_livro, livro_data):
    livro = Livro.query.get(id_livro)  # Busca o livro pelo ID

    if not livro:  # Se o livro não for encontrado, retorna erro
        response = make_response(
            json.dumps({'mensagem': 'Livro não encontrado.'}, ensure_ascii=False),
            404  # Código HTTP 404 para "Não encontrado"
        )
        response.headers['Content-Type'] = 'application/json'  # Garante que a resposta seja em JSON
        return response

    # Valida se todos os campos obrigatórios foram fornecidos
    if not all(key in livro_data for key in ['titulo', 'genero', 'paginas', 'ano_lancamento', 'autor']):
        response = make_response(
            json.dumps({'mensagem': 'Dados inválidos. Título, gênero, número de páginas, ano de lançamento e autor são obrigatórios'}, ensure_ascii=False),
            400  # Código HTTP 400 para requisição inválida
        )
        response.headers['Content-Type'] = 'application/json'  # Define que a resposta é em JSON
        return response

    livro.titulo=livro_data['titulo']
    livro.genero=livro_data['genero']
    livro.paginas=livro_data['paginas']
    livro.ano_lancamento=livro_data['ano_lancamento']
    livro.autor=livro_data['autor']


    db.session.commit()  # Confirma a atualização no banco de dados


    # Retorna a resposta com os dados do livro atualizado
    response = make_response(
        json.dumps({
            'mensagem': 'Livro atualizado com sucesso.',
            'livro': livro.json()
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'  # Define que a resposta é em JSON
    return response


# DELETE
def delete_livro(livro_id):
    
    confirmacao = request.args.get('confirmacao')
    
    if confirmacao != 'True':
        response = make_response(
            json.dumps({'mensagem': 'Confirmação necessária para excluir o livro.'}, ensure_ascii=False),
             400       
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    livro = Livro.query.get(livro_id)
    if not livro:
        response = make_response(
            json.dumps({'mensagem': 'Livro não encontrado.'}, ensure_ascii=False),
            404
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    db.session.delete(livro)
    db.session.commit()

    response = make_response(
        json.dumps({'mensagem': 'Livro excluído com sucesso.'}, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'
    return response

