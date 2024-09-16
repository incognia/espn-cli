import requests
import json
from prettytable import PrettyTable
from datetime import datetime
import pytz

# Función para obtener los datos de la API
def obtener_datos(fecha):
    url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates={fecha}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error al obtener los datos")
        return None

# Función para convertir la hora a diferentes zonas horarias
def convertir_hora(fecha_hora, zona_horaria):
    formato = "%Y-%m-%dT%H:%MZ"
    dt = datetime.strptime(fecha_hora, formato)
    dt = dt.replace(tzinfo=pytz.utc)
    return dt.astimezone(pytz.timezone(zona_horaria)).strftime("%H:%M")

# Función para imprimir los marcadores en una tabla
def imprimir_marcadores(datos):
    if datos:
        # Crear la tabla
        tabla = PrettyTable()
        tabla.field_names = ["Equipo", "Marcador", "Hora (EDT)", "Hora (CST)"]
        
        # Recorrer los eventos y extraer los detalles
        events = datos.get('events', [])
        if events:
            fecha_evento = events[0].get('date', 'Unknown').split('T')[0]
            semana = events[0].get('week', {}).get('number', 'Unknown')
            
            # Mostrar la fecha y la semana una sola vez
            print(f"\nFecha: {fecha_evento} | Semana: {semana}\n")
            
            for event in events:
                competition = event.get('competitions', [])[0]
                competitors = competition.get('competitors', [])
                hora_edt = convertir_hora(event.get('date', 'Unknown'), 'America/New_York')
                hora_cst = convertir_hora(event.get('date', 'Unknown'), 'America/Mexico_City')
                
                for team in competitors:
                    team_name = team.get('team', {}).get('displayName', 'Unknown')
                    score = team.get('score', '0')
                    tabla.add_row([team_name, score, hora_edt, hora_cst])
                
                # Añadir una línea de división después de cada partido
                tabla.add_row(["-"*10, "-"*10, "-"*10, "-"*10])
        
        # Imprimir la tabla
        print(tabla)

# Pedir la fecha de consulta de forma interactiva
fecha_consulta = input("Introduce la fecha de consulta (formato YYYYMMDD): ")

# Obtener los datos y imprimir los marcadores
datos = obtener_datos(fecha_consulta)
imprimir_marcadores(datos)
