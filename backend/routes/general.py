from flask import Blueprint, jsonify, send_from_directory, current_app
import os

general_blueprint = Blueprint('general', __name__)

@general_blueprint.route('/api/server-info', methods=['GET'])
def server_info():
    info = {
        "server_name": "ChefGPT",
        "version": "1.0.0",
        "status": "Running"
    }
    return jsonify(info)

@general_blueprint.route('/', defaults={'path': ''})
@general_blueprint.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(current_app.static_folder, path)):
        return send_from_directory(current_app.static_folder, path)
    else:
        return send_from_directory(current_app.template_folder, 'index.html')
