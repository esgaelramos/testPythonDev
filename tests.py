import uuid
import unittest
import json
from click.testing import CliRunner

from main import app
from cli import login

# tests for endpoints
class TestLoginEndPoint(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_successful_login(self):
        # Realizamos una petición POST con credenciales correctas
        response = self.client.post('/api/Seguridad/login/', data=json.dumps({'usuario': 'testuser', 'contrasena': 'testpass'}), content_type='application/json')

        # Verificamos que la respuesta sea un JSON válido
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('estado', data)
        self.assertIn('description', data)
        self.assertIn('token', data)

        # Verificamos que el token sea un UUID válido
        self.assertTrue(isinstance(data['token'], str))
        uuid.UUID(data['token'])

    def test_failed_login(self):
        # Realizamos una petición POST con credenciales incorrectas
        response = self.client.post('/api/Seguridad/login/', data=json.dumps({'usuario': 'testuser', 'contrasena': 'wrongpass'}), content_type='application/json')

        # Verificamos que la respuesta sea un JSON válido
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('estado', data)
        self.assertIn('description', data)
        self.assertFalse(data['estado'])
        self.assertEqual(data['description'], 'Usuario o contrasena incorrectos')


# tests for cli 
class TestCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_cli_login_x(self):
        result = self.runner.invoke(login, ['--usuario', 'testuserx', '--contrasena', 'testpassx', '--url', 'http://localhost:5000/api/Seguridad/login/'])
        self.assertEqual(result.exit_code, 0)

    def test_cli_login_success(self):
        result = self.runner.invoke(login, ['-u', 'testuser', '-p', 'testpass'])
        self.assertEqual(result.exit_code, 0)
        # import pdb; pdb.set_trace()
        self.assertIn('Autenticación exitosa. Token generado:', result.output)

    def test_cli_login_invalid(self):
        result = self.runner.invoke(login, ['-u', 'invaliduser', '-p', 'invalidpass'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Error de autenticación', result.output)

if __name__ == '__main__':
    unittest.main()