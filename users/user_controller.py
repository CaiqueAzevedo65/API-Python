from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from user_model import UserModel

class UserController:

    @staticmethod
    def register_user(data):
        
        username = data.get('username')
        
        password = data.get('password')
        
        if not username or not password:
            return {"error": "Nome de usuário e senha são obrigatórios"}, 400
        
        
        hashed_password = generate_password_hash(password)
        

        if UserModel.create_user(username, hashed_password):
            return {"message": "Usuário registrado com sucesso"}, 201
        
        return {"error": "Nome de usuário já existe"}, 400
    
    @staticmethod
    def login_user(data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {"error": "Nome de usuário e senha são obrigatórios"}, 400
        
        user = UserModel.find_by_username(username)

        if user and check_password_hash(user['password'], password):
            access_token = create_access_token(identity=str(user['id']))
            return {"access_token": access_token}, 200
        
        return {"error": "Nome de usuário ou senha inválidos"}, 401


    @staticmethod
    def get_user(user_id):

        user = UserModel.find_by_id(user_id)

        if user:
            return{"id": user["id"],"username": user["username"]}, 200
        
        return {"error": "Usuário não encontrado"}, 404
    
    @staticmethod
    def update_user(user_id, data):

        username = data.get('username')
        password = data.get('password')

        if not username and not password:
            return {"error": "Informe ao menos um campo para atualizar"}, 400
        
        hashed_password = generate_password_hash(password) if password else None

        UserModel.update_user(user_id, username, hashed_password)
        
        return {"message": "Usuário atualizado com sucesso"}, 200
    
    @staticmethod
    def delete_user(user_id):

        UserModel.delete_user(user_id)

        return {"message": "Usuário deletado com sucesso"}