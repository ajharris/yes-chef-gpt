import os
from openai import OpenAI
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

chatgpt_blueprint = Blueprint('chatgpt', __name__)

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@chatgpt_blueprint.route('/chatgpt', methods=['POST'])
def get_chatgpt_response():
    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    try:
        # Send the prompt to the OpenAI API using the new API interface
        response = client.chat.completions.create(
            model="gpt-4",  # Use GPT-3.5 turbo or GPT-4
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract the message content
        chatgpt_response = response.choices[0].message.content.strip()

        return jsonify({"response": chatgpt_response}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
