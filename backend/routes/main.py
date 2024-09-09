from flask import Blueprint, jsonify

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "API is running"}), 200
