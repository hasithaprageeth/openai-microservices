from flask import Flask, request, jsonify
from config import SQLConfig
from authentication import requires_auth
from openai_edit_client import get_edit_response
from models import db

app = Flask(__name__)
app.config.from_object(SQLConfig)

with app.app_context():
    db.init_app(app)
    db.create_all()


@app.route('/')
def index():
    return 'Edit Service is running.'


@app.route('/edit', methods=['POST'])
@requires_auth
def edit():
    data = request.get_json()
    try:
        if not data.get('instruction'):
            raise ValueError("Please provide a valid value for 'instruction' parameter. "
                             "The value should not be null or empty.")
        if not data.get('prompt'):
            raise ValueError("Please provide a valid value for 'prompt' parameter. "
                             "The value should not be null or empty.")
        instruction = data.get('instruction')
        prompt = data.get('prompt')

        # create a new database session
        with db.session() as session:
            response = get_edit_response(instruction, prompt, session)

        return jsonify(response.__dict__)
    except ValueError as e:
        return jsonify({'Error': str(e)}), 400
    except Exception as e:
        return jsonify({'Internal Error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=8000)
