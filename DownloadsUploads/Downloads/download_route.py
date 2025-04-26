from flask import Blueprint

from DownloadsUploads.Downloads.download_controller import DownloadController

dowload_bp = Blueprint('dowload_bp', __name__)

@dowload_bp.route('/download/<filename>', methods=['GET'])
def dowload_file(filename):
    return DownloadController.download_files(filename)