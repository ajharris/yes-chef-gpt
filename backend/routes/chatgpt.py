import openai
from flask import Blueprint, request, jsonify
from flask_login import login_required
import time

chatgpt_blueprint = Blueprint('chatgpt', __name__)

@chatgpt_blueprint.route('/query', methods=['POST'])
@login_required
def query_chatgpt():
    data = request.get_json()
    
    if not data or not data.get('prompt'):
        return jsonify({'error': 'Prompt is required'}), 400
    
    prompt = data.get('prompt')
    
    try:
        # Track time to calculate query duration
        start_time = time.time()

        # Make the request to OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )

        # Calculate query duration
        duration = time.time() - start_time

        # Return the response with duration and the completion text
        return jsonify({
            'response': response.choices[0].text.strip(),
            'duration': duration
        }), 200

    except openai.error.OpenAIError as e:
        # Catch any errors from OpenAI API
        return jsonify({'error': f'OpenAI API error: {str(e)}'}), 500

    except Exception as e:
        # Catch any unexpected server errors
        return jsonify({'error': f'Server error: {str(e)}'}), 500
