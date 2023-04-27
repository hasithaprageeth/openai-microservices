from flask import Flask, request, jsonify
from config import SQLConfig
from authentication import requires_auth
from openai_completions_client import get_completion_response
from models import db

app = Flask(__name__)
app.config.from_object(SQLConfig)

with app.app_context():
    db.init_app(app)
    db.create_all()


@app.route('/completions/health')
def index():
    return 'Completions Service is running.'


@app.route('/completions', methods=['POST'])
@requires_auth
def chat():
    data = request.get_json()
    try:
        if not data.get('prompt'):
            raise ValueError("Please provide a valid value for 'prompt' parameter. "
                             "The value should not be null or empty.")

        # create a new database session
        with db.session() as session:
            response = get_completion_response(data['prompt'], session)

        return jsonify(response.__dict__)
    except ValueError as e:
        return jsonify({'Error': str(e)}), 400
    except Exception as e:
        return jsonify({'Internal Error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=8000)
