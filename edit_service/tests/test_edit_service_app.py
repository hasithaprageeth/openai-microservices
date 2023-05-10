import unittest
import json
import os
from unittest.mock import patch
from edit_service.tests import test_utility
from edit_service.edit_response import EditResponse


class EditServiceTest(unittest.TestCase):
    def setUp(self):
        test_utility.setUpEnvVariables()
        os.environ["MYSQL_DATABASE"] = os.getenv('EDIT_MYSQL_DATABASE')

        from edit_service.app import app
        app.testing = True
        self.app = app.test_client()

    def test_edit_health(self):
        response = self.app.get('/edit/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Edit Service is running. . This is a new change')

    def test_edit_without_auth(self):
        data = {
            'instruction': 'test_instruction',
            'prompt': 'test_prompt'
        }
        response = self.app.post('/edit', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_edit_invalid_data(self):
        data = {
            'instruction': '',
            'prompt': ''
        }
        headers = {
            'Authorization': f'Bearer {test_utility.getApiKey()}'
        }
        response = self.app.post('/edit', data=json.dumps(data), headers=headers, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please provide a valid value for', response.data.decode('utf-8'))

    def test_edit_valid_data(self):
        with patch('edit_service.app.get_edit_response') as mock_get_edit_response:
            mock_get_edit_response.return_value = EditResponse('test_prompt', 'test_edited_text_response')
            data = {
                'instruction': 'test_instruction',
                'prompt': 'test_prompt'
            }
            headers = {
                'Authorization': f'Bearer {test_utility.getApiKey()}'
            }
            response = self.app.post('/edit', data=json.dumps(data), headers=headers, content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertIn('test_prompt', response.data.decode('utf-8'))
            self.assertIn('test_edited_text_response', response.data.decode('utf-8'))
            mock_get_edit_response.assert_called_once()