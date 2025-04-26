import os
import logging
from flask import jsonify, request
from werkzeug.utils import secure_filename
from datetime import datetime

LOG_FILE = 'upLoad.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

PASTA_UPLOAD = 'uploads'
EXTENSOES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt'}
TAMANHO_MAXIMO_ARQUIVO = 10*1048576 # 10MB

if not os.path.exists(PASTA_UPLOAD):
    os.makedirs(PASTA_UPLOAD)

class UploadController:
    @staticmethod
    def arquivo_permitido(arquivo):
        return '.' in arquivo and arquivo.rsplit('.',1)[1].lower() in EXTENSOES_PERMITIDAS

    @staticmethod
    def upload_file():
        if 'file' not in request.files:
            logging.warning('Falha no upload: Nennhum arquivo enviado')
            return jsonify({"error": "Nennhum arquivo enviado"}), 400
        
        arquivo = request.files['file']
        
        if arquivo.filename == 'file':
            logging.warning('Falha no upload: Nome do arquivo inválido')
            return jsonify({"error": "Nome do arquivo inválido"}), 400

        if request.content_length > TAMANHO_MAXIMO_ARQUIVO:
            logging.warning(f'Falha no upload: {arquivo.filename} - Excede o tamanho máximo de 500 KB')
            return jsonify({"error": "Excede o tamanho máximo de 10MB (10000kb)"}), 400

        if arquivo and UploadController.arquivo_permitido(arquivo.filename):
            nome_arquivo = secure_filename(arquivo.filename)
            caminho_arquivo = os.path.join(PASTA_UPLOAD, nome_arquivo)

            if os.path.exists(caminho_arquivo):
                logging.warning(f'Falha no upload: {nome_arquivo} - Arquivo já existe')
                return jsonify({
                    "error": "Arquivo com o mesmo nome já existe",
                    "arquivo": nome_arquivo
                }), 400

            arquivo.save(caminho_arquivo)
            ip_usuario = request.remote_addr
            logging.info(f'Upload bem-sucedido: {nome_arquivo} | IP: {ip_usuario} | Data: {datetime.now()}')
            return jsonify({
                "msg": "Arquivo salvo com sucesso",
                "arquivo": nome_arquivo
            }), 200

        else:
            logging.warning(f'Falha no upload: {arquivo.filename} - Tipo de arquivo não permitido')
            return jsonify({
                "error": "Tipo de arquivo não permitido",
                "tipo_permitido": list(EXTENSOES_PERMITIDAS)
            }), 400