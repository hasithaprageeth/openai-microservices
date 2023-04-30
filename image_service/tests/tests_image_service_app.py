import unittest
import json
import os
import test_utility
from unittest.mock import patch
from image_service.image_response import ImageResponse


class ImageServiceTest(unittest.TestCase):
    def setUp(self):
        test_utility.setUpEnvVariables()
        os.environ["MYSQL_DATABASE"] = os.getenv('IMAGE_MYSQL_DATABASE')

        from image_service.app import app
        app.testing = True
        self.app = app.test_client()

    def test_image_health(self):
        response = self.app.get('/image/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Image Service is running.')

    def test_image_without_auth(self):
        data = {
            'prompt': 'test_prompt'
        }
        response = self.app.post('/image', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_image_invalid_data(self):
        data = {
            'prompt': ''
        }
        headers = {
            'Authorization': f'Bearer {test_utility.getApiKey()}'
        }
        response = self.app.post('/image', data=json.dumps(data), headers=headers, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please provide a valid value for', response.data.decode('utf-8'))

    def test_image_valid_data(self):
        with patch('image_service.app.get_image_response') as mock_get_image_response:
            mock_get_image_response.return_value = ImageResponse('test_prompt', 'test_image_url_response')
            data = {
                'prompt': 'test_prompt'
            }
            headers = {
                'Authorization': f'Bearer {test_utility.getApiKey()}'
            }
            response = self.app.post('/image', data=json.dumps(data), headers=headers, content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertIn('test_prompt', response.data.decode('utf-8'))
            self.assertIn('test_image_url_response', response.data.decode('utf-8'))
            mock_get_image_response.assert_called_once()