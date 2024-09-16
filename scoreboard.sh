#!/bin/bash

# Verificar si curl está instalado
if ! command -v curl &> /dev/null; then
    echo "curl no está instalado. Por favor, instálalo y vuelve a intentarlo."
    exit 1
fi

# Verificar si jq está instalado
if ! command -v jq &> /dev/null; then
    echo "jq no está instalado. Por favor, instálalo y vuelve a intentarlo."
    exit 1
fi

# Eliminar el archivo scoreboard.json si existe
[ -f scoreboard.json ] && rm scoreboard.json

# Descargar el archivo usando curl
curl -f -o scoreboard.raw https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard
if [ $? -ne 0 ]; then
    echo "Error al descargar el archivo."
    exit 1
fi

# Procesar el archivo con jq
jq . scoreboard.raw > scoreboard.json
if [ $? -ne 0 ]; then
    echo "Error al procesar el archivo con jq."
    exit 1
fi

# Asegurarse de que el archivo temporal se elimine
trap 'rm -f scoreboard.raw' EXIT
