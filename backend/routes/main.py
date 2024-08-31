from flask import Blueprint, jsonify, send_from_directory, current_app
import os

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/api/server-info', methods=['GET'])
def server_info():
    info = {
        "server_name": "ChefGPT",
        "version": "1.0.0",
        "status": "Running"
    }
    return jsonify(info)

@main_blueprint.route('/about')
def about():
    return "About ChefGPT"

@main_blueprint.route('/', defaults={'path': ''})
@main_blueprint.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(current_app.static_folder, path)):
        return send_from_directory(current_app.static_folder, path)
    else:
        return send_from_directory(current_app.template_folder, 'index.html')
