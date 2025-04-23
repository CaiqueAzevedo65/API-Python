from flask import Blueprint, request 
from controller.filme_controller import *

filme_route = Blueprint('filme_route',__name__)

# rotas GET
@filme_route.route('/Filme', methods=['GET'])
def buscar_todos_filmes():
    return get_filmes()

@filme_route.route('/Filme/<int:id>', methods=['GET'])
def buscar_filmes_id(id):
    return get_filmes_id(id)

@filme_route.route('/Filme/First', methods=['GET'])
def buscar_filme_first():
    return get_first_filme()

@filme_route.route('/Filme/Genero/<genero>', methods=['GET'])
def buscar_filme_filter_genero(genero):
    return get_filmes_filter_genero(genero)

@filme_route.route('/Filme/Diretor/<diretor>', methods=['GET'])
def buscar_filme_filter_by_diretor(diretor):
    return get_filmes_filter_by_diretor(diretor)

@filme_route.route('/Filme/Ordenar', methods=['GET'])
def buscar_filme_order_by_duracao():
    return get_filmes_order_by_duracao()

@filme_route.route('/Filme/Limite', methods=['GET'])
def buscar_filmes_limitados():
    return get_filmes_limitados()

@filme_route.route('/Filme/Offset', methods=['GET'])
def buscar_filmes_offset():
    return get_filmes_offset(offset=3)

@filme_route.route('/Filme/Contar', methods=['GET'])
def contar_todos_filmes():
    return contar_filmes()

@filme_route.route('/Filme/Paginar', methods=['GET'])
def buscar_filmes_paginados_pagina1():
    return buscar_filmes_paginados_1()

@filme_route.route('/Filme/Generos', methods=['GET'])
def buscar_generos_distintos():
    return buscar_generos_filmes_diferentes()

@filme_route.route('/Filme/Contagem/generos', methods=['GET'])
def contagem_generos():
    return contagem_generos_filmes()

@filme_route.route('/Filme/Titulos', methods=['GET'])
def buscar_so_titulos():
    return buscar_titulos_filmes()

@filme_route.route('/Filme/Existe/<titulo>', methods=['GET'])
def existe(titulo):
    return buscar_exist_filmes(titulo)


# rotas POST
@filme_route.route('/Filme', methods=['POST'])
def postar_filmes():
    return create_filme(request.json)


# rotas PUT
@filme_route.route('/Filme/<int:filme_id>', methods=['PUT'])
def atualizar_filme_por_id(filme_id):
    return update_filme(filme_id, request.json)


# rotas DELETE
@filme_route.route('/Filme/<int:filme_id>/<confirmacao>', methods=['DELETE'])
def deletar_filme(filme_id,confirmacao):
    if confirmacao != "True":
        return "Para realizar o DELETE é necessário a confirmação"
    return delete_filme(filme_id)
