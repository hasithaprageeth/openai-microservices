import unittest
import json
import os
from unittest.mock import patch
from chat_service.tests import test_utility
from chat_service.chat_response import ChatResponse


class ChatServiceTest(unittest.TestCase):
    def setUp(self):
        test_utility.setUpEnvVariables()
        os.environ["MYSQL_DATABASE"] = os.getenv('CHAT_MYSQL_DATABASE')

        from chat_service.app import app
        app.testing = True
        self.app = app.test_client()

    def test_chat_health(self):
        response = self.app.get('/chat/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Chat Service is running.')

    def test_chat_without_auth(self):
        data = {
            'role': 'user',
            'prompt': 'test_prompt'
        }
        response = self.app.post('/chat', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_chat_invalid_data(self):
        data = {
            'role': '',
            'prompt': 'test_prompt'
        }
        headers = {
            'Authorization': f'Bearer {test_utility.getApiKey()}'
        }
        response = self.app.post('/chat', data=json.dumps(data), headers=headers, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please provide a valid value for', response.data.decode('utf-8'))

    def test_chat_valid_data(self):
        with patch('chat_service.app.get_chat_response') as mock_get_chat_response:
            mock_get_chat_response.return_value = ChatResponse('assistant', 'test_response')
            data = {
                'role': 'user',
                'prompt': 'test_prompt'
            }
            headers = {
                'Authorization': f'Bearer {test_utility.getApiKey()}'
            }
            response = self.app.post('/chat', data=json.dumps(data), headers=headers, content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertIn('role', response.data.decode('utf-8'))
            self.assertIn('response', response.data.decode('utf-8'))
            mock_get_chat_response.assert_called_once()