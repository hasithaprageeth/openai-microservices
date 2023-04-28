import os
import base64
import yaml


def setUpEnvVariables():
    secrets_file = os.path.abspath('../../dev/secrets.yaml')

    # Load the environment variables
    with open(secrets_file, 'r') as f:
        secrets = yaml.safe_load(f)

    for key, value in secrets['data'].items():
        decoded_value = base64.b64decode(value).decode('utf-8')

        match key:
            case 'openai-api-key':
                os.environ["OPENAI_API_KEY"] = decoded_value
            case 'database_host':
                os.environ["MYSQL_HOST"] = decoded_value
            case 'database_port':
                os.environ["MYSQL_PORT"] = decoded_value
            case 'database_user':
                os.environ["MYSQL_USER"] = decoded_value
            case 'database_pwd':
                os.environ["MYSQL_PASSWORD"] = decoded_value
            case 'chat_database':
                os.environ["CHAT_MYSQL_DATABASE"] = decoded_value
            case 'edit_database':
                os.environ["EDIT_MYSQL_HOST"] = decoded_value
            case 'completion_database':
                os.environ["COMPLETION_MYSQL_HOST"] = decoded_value
            case 'image_database':
                os.environ["IMAGE_MYSQL_HOST"] = decoded_value
            case 'api-key':
                os.environ["API_KEY"] = decoded_value


def getApiKey():
    encoded_value = 'eyJhbGciOiJIUzI1NiJ9.e30.5sMLJgsil83Q8JJEtLYJxJp6MkRqQofMUhoDcaRfv74'
    return encoded_value