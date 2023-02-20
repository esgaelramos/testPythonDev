import uuid
import sqlite3
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)
DB_PATH = 'dbtestdev.sqlite'

# Función para verificar las credenciales del usuario en la BD
def verify_user_credentials(user, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verificamos si las credenciales del usuario son correctas
    cursor.execute(f"SELECT * FROM UserAccess WHERE UserAccess='{user}' AND PassAccess='{password}'")
    row = cursor.fetchone()
    conn.close()
    return row

# Función para generar un nuevo token
def generate_token():
    return str(uuid.uuid4())

# Función para actualizar el token y su fecha de expiración en la BD
def update_token_in_db(user, token):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Actualizamos el registro en la BD con el nuevo token y fecha de expiración
    expiration_date = datetime.now() + timedelta(hours=1)
    cursor.execute(f"UPDATE UserAccess SET TokenAccess='{token}', ExpirationAcess='{expiration_date}' WHERE UserAccess='{user}'")
    conn.commit()
    conn.close()

# Endpoint para autenticación de usuario
@app.route('/api/Seguridad/login/', methods=['POST'])
def login():
    """
    Endpoint para autenticación de usuario
    ---
    consumes:
      - application/json
    parameters:
      - in: body
        name: user_credentials
        description: Credenciales del usuario para autenticación
        required: true
        schema:
          type: object
          properties:
            usuario:
              type: string
              description: Nombre de usuario
              example: testuser
            contrasena:
              type: string
              description: Contrasena del usuario
              example: testpass
    responses:
      200:
        description: Devuelve el token generado y su mensaje descriptivo
        schema:
          type: object
          properties:
            estado:
              type: boolean
              description: Indica si la autenticación fue exitosa
            description:
              type: string
              description: Mensaje descriptivo de la respuesta
            token:
              type: string
              description: Token generado, solo si la autenticación fue exitosa
    """
    # Obtenemos los datos de usuario y contraseña del 

    # Obtenemos los datos de usuario y contrasena del request
    user = request.json.get('usuario', '')
    password = request.json.get('contrasena', '')

    # Default las credenciales son incorrectas
    authen = jsonify({'estado': False, 'description': 'Usuario o contrasena incorrectos'})

    # Verificamos las credenciales del usuario en la BD
    if verify_user_credentials(user, password):
        # Generamos un nuevo token
        token = generate_token()

        # Actualizamos el token y la fecha de expiración en la BD
        update_token_in_db(user, token)

        # Devolvemos el token generado
        authen = jsonify({'estado': True, 'description': '', 'token': token})
    
    # Devolvemos la respuesta de autenticación 
    return authen

if __name__ == '__main__':
    app.run(debug=True)
