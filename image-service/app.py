from flask import Flask, request, jsonify
from config import SQLConfig
from authentication import requires_auth
from openai_image_client import get_image_response
from models import db

app = Flask(__name__)
app.config.from_object(SQLConfig)

with app.app_context():
    db.init_app(app)
    db.create_all()


@app.route('/')
def index():
    return 'Image Service is running.'


@app.route('/image', methods=['POST'])
@requires_auth
def image():
    data = request.get_json()
    try:
        if not data.get('prompt'):
            raise ValueError("Please provide a valid value for 'prompt' parameter. "
                             "The value should not be null or empty.")
        prompt = data.get('prompt')

        # create a new database session
        with db.session() as session:
            response = get_image_response(prompt, session)

        return jsonify(response.__dict__)
    except ValueError as e:
        return jsonify({'Error': str(e)}), 400
    except Exception as e:
        return jsonify({'Internal Error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=8000)
