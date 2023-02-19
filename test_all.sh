#!/bin/bash

# Prueba del script principal utilizando 'python'
echo "Activando la app principal"
python3 main.py &
sleep 2

# Ejecuta todas las pruebas unitarias
echo "\nEjecutando tests unitarios"
python3 -m unittest -v

# Prueba del CLI utilizando 'python'
echo "\nProbando el CLI"
python cli.py login -u testuser -p testpass

# Prueba del endpoint de autenticación utilizando 'curl'
echo "\nProbando el endpoint de autenticación"
curl -X POST -H "Content-Type: application/json" -d '{"usuario": "testuser", "contrasena": "testpass"}' http://localhost:5000/api/Seguridad/login/

# Detiene la aplicación Flask utilizando su nombre de proceso
pkill -f main.py

