import uuid
import unittest
import json
from main import app

# tests for endpoints
class TestLoginEndPoint(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_successful_login(self):
        # Creamos un usuario en la base de datos para probar la autenticación
        self.client.post('/api/Seguridad/crear_usuario/', data=json.dumps({'usuario': 'testuser', 'contrasena': 'testpass'}), content_type='application/json')

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

    def tearDown(self):
        # Eliminamos el usuario creado en la base de datos para las pruebas
        self.client.post('/api/Seguridad/eliminar_usuario/', data=json.dumps({'usuario': 'testuser'}), content_type='application/json')

# tests for cli 


if __name__ == '__main__':
    unittest.main()