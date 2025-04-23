import sqlite3
from db import get_db_connection

class FormularioModel:
    # POST
    @staticmethod
    def create_form(user_id, nome, email, data_nascimento, cpf, genero):
        conn = get_db_connection()
        try: 
            conn.execute('INSERT INTO formularios (user_id, nome, email, data_nascimento, cpf, genero) VALUES (?, ?, ?, ?, ?, ?)', (user_id, nome, email, data_nascimento, cpf, genero))
            conn.commit()
        except sqlite3.IntegrityError:
            return None
        
        finally:
            conn.close()
        
        return True
    

    # GET
    @staticmethod
    def find_form_by_user_id(user_id):
        conn = get_db_connection()
        formulario = conn.execute('SELECT * FROM formularios WHERE user_id = ?', (user_id,)).fetchall()
        conn.close()
        return formulario
    
    @staticmethod
    def find_by_email(email):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM formularios WHERE email = ?', (email,)).fetchone()
        conn.close()
        return user
    

    

    
    # @staticmethod
    # def update_user(user_id,username=None, password=None):
    #     conn = get_db_connection()

    #     if username:
    #         conn.execute('UPDATE users SET username = ? WHERE id = ?', (username, user_id))
        
    #     if password:
    #         conn.execute('UPDATE users SET password = ? WHERE id = ?', (password, user_id))

    #     conn.commit()
    #     conn.close()

    # @staticmethod
    # def delete_user(user_id):
    #     conn = get_db_connection()
    #     conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    #     conn.commit()
    #     conn.close()