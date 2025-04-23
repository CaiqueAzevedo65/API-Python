from flask import Blueprint, request 
from controller.livro_controller import *

livro_route = Blueprint('livro_route',__name__)

# rotas GET
@livro_route.route('/Livro', methods=['GET'])
def buscar_todos_livros():
    return get_livros()

@livro_route.route('/Livro/<int:id>', methods=['GET'])
def buscar_livros_id(id):
    return get_livros_id(id)

@livro_route.route('/Livro/First', methods=['GET'])
def buscar_livro_first():
    return get_first_livro()

@livro_route.route('/Livro/Genero/<genero>', methods=['GET'])
def buscar_livro_filter_genero(genero):
    return get_livros_filter_genero(genero)

@livro_route.route('/Livro/Diretor/<diretor>', methods=['GET'])
def buscar_livro_filter_by_diretor(diretor):
    return get_livros_filter_by_diretor(diretor)

@livro_route.route('/Livro/Ordenar', methods=['GET'])
def buscar_livro_order_by_duracao():
    return get_livros_order_by_duracao()

@livro_route.route('/Livro/Limite', methods=['GET'])
def buscar_livros_limitados():
    return get_livros_limitados()

@livro_route.route('/Livro/Offset', methods=['GET'])
def buscar_livros_offset():
    return get_livros_offset(offset=3)

@livro_route.route('/Livro/Contar', methods=['GET'])
def contar_todos_livros():
    return contar_livros()

@livro_route.route('/Livro/Paginar', methods=['GET'])
def buscar_livros_paginados_pagina1():
    return buscar_livros_paginados_1()

@livro_route.route('/Livro/Generos', methods=['GET'])
def buscar_generos_distintos():
    return buscar_generos_livros_diferentes()

@livro_route.route('/Livro/Contagem/generos', methods=['GET'])
def contagem_generos():
    return contagem_generos_livros()

@livro_route.route('/Livro/Titulos', methods=['GET'])
def buscar_so_titulos():
    return buscar_titulos_livros()

@livro_route.route('/Livro/Existe/<titulo>', methods=['GET'])
def existe(titulo):
    return buscar_exist_livros(titulo)


# rotas POST
@livro_route.route('/Livro', methods=['POST'])
def postar_livros():
    return create_livro(request.json)


# rotas PUT
@livro_route.route('/Livro/<int:livro_id>', methods=['PUT'])
def atualizar_livro_por_id(livro_id):
    return update_livro(livro_id, request.json)


# rotas DELETE
@livro_route.route('/Livro/<int:livro_id>', methods=['DELETE'])
def deletar_livro(livro_id):
    return delete_livro(livro_id)
