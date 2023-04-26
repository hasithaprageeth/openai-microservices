from flask import Flask, request, jsonify
from openai_edit_client import get_edit_response
from common.authentication import requires_auth

app = Flask(__name__)


@app.route('/edit', methods=['POST'])
@requires_auth
def edit():
    data = request.get_json()
    if not data.get('instruction'):
        raise ValueError("Please provide a valid value for 'instruction' parameter. "
                         "The value should not be null or empty.")
    if not data.get('prompt'):
        raise ValueError("Please provide a valid value for 'prompt' parameter. "
                         "The value should not be null or empty.")

    instruction = data.get('instruction')
    prompt = data.get('prompt')
    response = get_edit_response(instruction, prompt)
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
