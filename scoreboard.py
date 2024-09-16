#!/usr/bin/python3

import os
import requests
import json

# Eliminar el archivo scoreboard.json si existe
if os.path.exists('scoreboard.json'):
    os.remove('scoreboard.json')

# Descargar el archivo usando requests
try:
    response = requests.get('https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard')
    response.raise_for_status()
    with open('scoreboard.raw', 'wb') as file:
        file.write(response.content)
except requests.RequestException as e:
    print(f"Error al descargar el archivo: {e}")
    exit(1)

# Procesar el archivo con la biblioteca json
try:
    with open('scoreboard.raw', 'r') as raw_file:
        data = json.load(raw_file)
    with open('scoreboard.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
except json.JSONDecodeError as e:
    print(f"Error al procesar el archivo: {e}")
    exit(1)

# Asegurarse de que el archivo temporal se elimine
os.remove('scoreboard.raw')
