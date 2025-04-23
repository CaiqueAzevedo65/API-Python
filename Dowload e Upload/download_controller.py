from flask import jsonify, send_from_directory

UPLOAD_FOLDER = 'uploads'

class DownloadController:
    @staticmethod
    def download_files(file):
        try:
            return send_from_directory(UPLOAD_FOLDER, file, as_attachment=True)
        except FileNotFoundError:
            return jsonify({"error": "File not found"}), 404 



