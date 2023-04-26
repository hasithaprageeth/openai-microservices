from flask import Flask, request, jsonify
from openai_completions_client import get_completion_response
from common.authentication import requires_auth

app = Flask(__name__)


@app.route('/completions', methods=['POST'])
@requires_auth
def chat():
    data = request.get_json()
    if not data.get('prompt'):
        raise ValueError("Please provide a valid value for 'prompt' parameter. "
                         "The value should not be null or empty.")

    response = get_completion_response(data['prompt'])
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
