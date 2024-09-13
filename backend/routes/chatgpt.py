import openai
from flask import Blueprint, request, jsonify
from flask_login import login_required

chatgpt_blueprint = Blueprint('chatgpt', __name__)

@chatgpt_blueprint.route('/query', methods=['POST'])
@login_required
def query_chatgpt():
    data = request.get_json()
    prompt = data.get('prompt')

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )

    return jsonify(response.choices[0].text)
