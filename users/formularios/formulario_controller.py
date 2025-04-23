import json
from formularios.formulario_model import FormularioModel
from flask import make_response

class FormularioController:
    @staticmethod
    def register_form(user_id,data):      
        nome = data.get('nome')
        email = data.get('email')
        data_nascimento = data.get('data_nascimento')
        cpf = data.get('cpf')
        genero = data.get('genero')

        if not nome or not email or not data_nascimento or not cpf or not genero:
            return {"error": "Cadastro de todos os campos é obrigatório"}, 400
        
        
        formulario = FormularioModel.create_form(user_id, nome, email, data_nascimento, cpf, genero)
        if formulario:
            return {"message": "Formulário registrado com sucesso"}, 201
        else:
            return {"error": "Erro ao criar o formulário"}, 500

    @staticmethod
    def get_form(user_id):  
        formularios = FormularioModel.find_form_by_user_id(user_id)

        if formularios:
            formulario_list = [
                {
                    "id": formularios["id"],
                    "user_id": formularios["user_id"],
                    "nome": formularios['nome'],
                    "email": formularios['email'],
                    "data_nascimento": formularios['data_nascimento'],
                    "cpf": formularios['cpf'],
                    "genero": formularios['genero']
                }
                for formularios in formularios
            ]

            response = make_response(
                json.dumps(formulario_list, sort_keys=False, ensure_ascii=False)
            )
            response.headers['Content-Type'] = 'application/json'
            return response, 200
        
        return {"msg": f"O usuário {user_id} requerido não possui formulários"}

    @staticmethod
    def get_form_by_email(email):  
        formulario = FormularioModel.find_by_email(email)

        if formulario:
            response = make_response(
                json.dumps({
                    "id": formulario["id"],
                    "user_id": formulario["user_id"],
                    "nome": formulario['nome'],
                    "email": formulario['email'],
                    "data_nascimento": formulario['data_nascimento'],
                    "cpf": formulario['cpf'],
                    "genero": formulario['genero']
                }, sort_keys=False, ensure_ascii=False)
            )
            response.headers['Content-Type'] = 'application/json'
            return response, 200
        
        return {"msg": f"Não existem formulários com o email: {email}"}