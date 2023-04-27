import json
import unittest
from app import app


class TestChatService(unittest.TestCase):


    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Chat Service is running.')

    def test_chat_with_valid_input(self):
        data = {
            "role": "user",
            "prompt": "Who won the world series in 2020?"
        }
        headers = {
            "Authorization": "Bearer mytoken"
        }
        response = self.app.post('/chat', data=json.dumps(data), headers=headers,
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('response', json.loads(response.data.decode('utf-8')))

    def test_chat_with_missing_role_parameter(self):
        data = {
            "prompt": "Hi, can you help me with my account?"
        }
        headers = {
            "Authorization": "Bearer mytoken"
        }
        response = self.app.post('/chat', data=json.dumps(data), headers=headers,
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Error', json.loads(response.data.decode('utf-8')))

    def test_chat_with_missing_prompt_parameter(self):
        data = {
            "role": "customer"
        }
        headers = {
            "Authorization": "Bearer mytoken"
        }
        response = self.app.post('/chat', data=json.dumps(data), headers=headers,
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Error', json.loads(response.data.decode('utf-8')))

    def test_chat_with_invalid_token(self):
        data = {
            "role": "customer",
            "prompt": "Hi, can you help me with my account?"
        }
        headers = {
            "Authorization": "Bearer invalid_token"
        }
        response = self.app.post('/chat', data=json.dumps(data), headers=headers,
                                 content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('message', json.loads(response.data.decode('utf-8')))


if __name__ == '__main__':
    unittest.main()
