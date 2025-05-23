import sqlite3
from db import get_db_connection

class UploadModel:
    @staticmethod
    def save_file(filename, filepath):
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO uploads (filename, filepath) 
                VALUES (?, ?)", (filename, filepath)
            ''', (filename, filepath))        
            conn.commit()
        
        except sqlite3.IntegrityError:
            return None
        
        finally:
            conn.close()
        
        return True
    
    @staticmethod
    def find_by_filename(filename):
        conn = get_db_connection()
        file = conn.execute("SELECT * FROM uploads WHERE filename = ?", (filename,)).fetchone()
        conn.close()
        return file
    
    @staticmethod
    def delete_file(filename):
        conn = get_db_connection()
        conn.execute("DELETE FROM uploads WHERE filename = ?", (filename,))
        conn.commit()
        conn.close()
        return True