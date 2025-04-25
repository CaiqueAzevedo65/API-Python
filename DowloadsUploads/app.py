from flask import Flask
from db import init_db
from upload_route import upload_bp
from download_route import dowload_bp
import os 

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

init_db()

app.register_blueprint(upload_bp, url_prefix='/uploads')

app.register_blueprint(dowload_bp, url_prefix='/downloads')

if __name__ == '__main__':
    app.run(debug=True)