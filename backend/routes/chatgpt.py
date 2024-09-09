from flask import Blueprint, request, jsonify

chatgpt_blueprint = Blueprint('chatgpt', __name__)

@chatgpt_blueprint.route('/chatgpt', methods=['POST'])  # Make sure 'POST' is included
def get_chatgpt_response():
    data = request.json  # Get the JSON data from the request
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    # Simulate ChatGPT response
    response = {
        "response": f"Generated response for: {prompt}"
    }

    return jsonify(response), 200
