from flask import Flask, request, jsonify
from chat_service.config import SQLConfig
from chat_service.authentication import requires_auth
from chat_service.openai_chat_client import get_chat_response
from chat_service.models import db

app = Flask(__name__)
app.config.from_object(SQLConfig)

with app.app_context():
    db.init_app(app)
    db.create_all()


@app.route('/chat/health')
def chat_health():
    return 'Chat Service is running.'


@app.route('/chat', methods=['POST'])
@requires_auth
def chat():
    data = request.get_json()
    try:
        if not data.get('role'):
            raise ValueError("Please provide a valid value for 'role' parameter. "
                             "The value should not be null or empty.")
        if not data.get('prompt'):
            raise ValueError("Please provide a valid value for 'prompt' parameter. "
                             "The value should not be null or empty.")
        role = data.get('role')
        prompt = data.get('prompt')

        # create a new database session
        with db.session() as session:
            response = get_chat_response(role, prompt, session)

        return jsonify(response.__dict__)
    except ValueError as e:
        return jsonify({'Error': str(e)}), 400
    except Exception as e:
        return jsonify({'Internal Error': str(e)}), 500


if __name__ == '__main__':
    app.run()
