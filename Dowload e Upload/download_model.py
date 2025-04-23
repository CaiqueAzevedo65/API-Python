from db import get_db_connection

class DownloadModel:
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