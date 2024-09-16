#!/usr/bin/python3

import requests
from PIL import Image
from io import BytesIO
import os

# Preguntar la URL de la imagen
url = input("Introduce la URL de la imagen: ")

# Descargar la imagen
response = requests.get(url)
img = Image.open(BytesIO(response.content))

# Guardar la imagen temporalmente
temp_image_path = "/tmp/temp_image.png"
img.save(temp_image_path)

# Mostrar la imagen en la terminal usando chafa
os.system(f"chafa {temp_image_path}")

# Eliminar la imagen temporal
os.remove(temp_image_path)

