#!/bin/bash

if ! command -v curl &> /dev/null; then
    echo "curl no está instalado. Por favor, instálalo y vuelve a intentarlo."
    exit 1
fi

[ -f scoreboard.json ] && rm scoreboard.json

curl -f -o scoreboard.raw https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard
if [ $? -ne 0 ]; then
    echo "Error al descargar el archivo."
    exit 1
fi

if ! command -v jq &> /dev/null; then
    echo "jq no está instalado. Por favor, instálalo y vuelve a intentarlo."
    exit 1
fi

jq . scoreboard.raw > scoreboard.json
if [ $? -ne 0 ]; then
    echo "Error al procesar el archivo con jq."
    exit 1
fi

trap 'rm -f scoreboard.raw' EXIT
