import unittest
import json
import os
import test_utility
from unittest.mock import patch
from completions_service.completion_response import CompletionResponse


class CompletionsServiceTest(unittest.TestCase):
    def setUp(self):
        test_utility.setUpEnvVariables()
        os.environ["MYSQL_DATABASE"] = os.getenv('COMPLETION_MYSQL_DATABASE')

        from chat_service.app import app
        app.testing = True
        self.app = app.test_client()

    def test_completions_health(self):
        response = self.app.get('/completions/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Completions Service is running.')

    def test_completions_without_auth(self):
        data = {
            'prompt': 'test_prompt'
        }
        response = self.app.post('/completions', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_completions_invalid_data(self):
        data = {
            'prompt': ''
        }
        headers = {
            'Authorization': f'Bearer {test_utility.getApiKey()}'
        }
        response = self.app.post('/completions', data=json.dumps(data), headers=headers, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please provide a valid value for', response.data.decode('utf-8'))

    def test_completions_valid_data(self):
        with patch('completions_service.app.get_completion_response') as mock_get_completion_response:
            mock_get_completion_response.return_value = CompletionResponse('test_prompt', 'test_completed_response')
            data = {
                'prompt': 'test_prompt'
            }
            headers = {
                'Authorization': f'Bearer {test_utility.getApiKey()}'
            }
            response = self.app.post('/completions', data=json.dumps(data), headers=headers, content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertIn('test_prompt', response.data.decode('utf-8'))
            self.assertIn('test_completed_response', response.data.decode('utf-8'))
            mock_get_completion_response.assert_called_once()