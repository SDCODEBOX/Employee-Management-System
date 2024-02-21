import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from app import home, about, AddEmp, FetchData

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['DEBUG'] = False
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    @patch('app.render_template')
    def test_home(self, mock_render_template):
        with self.app.test_request_context('/'):
            home()
            mock_render_template.assert_called_once_with('AddEmp.html')

    @patch('app.render_template')
    def test_about(self, mock_render_template):
        with self.app.test_request_context('/about'):
            about()
            mock_render_template.assert_called_once_with('www.intellipaat.com')

    @patch('app.render_template')
    @patch('app.request')
    def test_AddEmp(self, mock_request, mock_render_template):
        mock_request.method = 'POST'
        mock_request.form = {
            'emp_id': '1',
            'first_name': 'John',
            'last_name': 'Doe',
            'pri_skill': 'Python',
            'location': 'New York',
            'emp_image_file': MagicMock(filename='test.jpg')
        }
        with patch('app.boto3.resource') as mock_boto3_resource:
            with self.app.test_request_context('/addemp'):
                response = AddEmp()
                mock_boto3_resource().Bucket().put_object.assert_called_once()
                mock_render_template.assert_called_once_with('AddEmpOutput.html', name='John Doe')

    @patch('app.render_template')
    @patch('app.request')
    def test_FetchData(self, mock_request, mock_render_template):
        mock_request.method = 'POST'
        mock_request.form = {'emp_id': '1'}
        with patch('app.boto3.client') as mock_boto3_client:
            mock_dynamodb_client = MagicMock()
            mock_dynamodb_client.get_item.return_value = {
                'Item': {'image_url': {'S': 'https://example.com/image.jpg'}}
            }
            mock_boto3_client.return_value = mock_dynamodb_client
            with self.app.test_request_context('/fetchdata'):
                response = FetchData()
                mock_render_template.assert_called_once_with('GetEmpOutput.html', id='1', fname=None, lname=None,
                                                              interest=None, location=None,
                                                              image_url='https://example.com/image.jpg')

if __name__ == '__main__':
    unittest.main()
