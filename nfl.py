#!/usr/bin/python3

import requests
import json
from prettytable import PrettyTable
from datetime import datetime
import pytz
import argparse

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
    try:
        formato = "%Y-%m-%dT%H:%MZ"
        dt = datetime.strptime(fecha_hora, formato)
        dt = dt.replace(tzinfo=pytz.utc)
        return dt.astimezone(pytz.timezone(zona_horaria)).strftime("%H:%M")
    except ValueError:
        return "Hora inválida"

# Función para imprimir los marcadores en una tabla
def imprimir_marcadores(datos):
    if datos:
        tabla = PrettyTable()
        tabla.field_names = ["Equipo", "Marcador", "Hora (EDT)", "Hora (CST)"]
        
        events = datos.get('events', [])
        if events:
            fecha_evento = events[0].get('date', 'Unknown').split('T')[0]
            semana = events[0].get('week', {}).get('number', 'Unknown')
            
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
                
                if event != events[-1]:
                    tabla.add_row(["-"*10, "-"*10, "-"*10, "-"*10])
        
        print(tabla)

# Función para validar la fecha de entrada
def validar_fecha(fecha):
    try:
        datetime.strptime(fecha, "%Y%m%d")
        return True
    except ValueError:
        return False

# Configuración de argumentos de línea de comandos
parser = argparse.ArgumentParser(description="Obtener marcadores de la NFL.")
parser.add_argument("-d", "--date", type=str, help="Fecha de consulta en formato YYYYMMDD")
parser.add_argument("-t", "--today", action="store_true", help="Usar la fecha de hoy")

args = parser.parse_args()

# Determinar la fecha de consulta
if args.today:
    fecha_consulta = datetime.now().strftime("%Y%m%d")
elif args.date:
    if validar_fecha(args.date):
        fecha_consulta = args.date
    else:
        print("Fecha inválida. Por favor, introduce una fecha en el formato YYYYMMDD.")
        exit(1)
else:
    fecha_consulta = input("Introduce la fecha de consulta (formato YYYYMMDD): ")
    if not validar_fecha(fecha_consulta):
        print("Fecha inválida. Por favor, introduce una fecha en el formato YYYYMMDD.")
        exit(1)

# Obtener los datos y imprimir los marcadores
datos = obtener_datos(fecha_consulta)
imprimir_marcadores(datos)
