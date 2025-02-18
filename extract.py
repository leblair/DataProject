import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()  #load env file
# Configuración de la API
URL = os.getenv('URL')
ENDPOINT_CATEGORIES = f"{URL}/categories/"
ENDPOINT_RECIPES = f"{URL}/recipes/"
ENDPOINT_RECIPE_DETAIL = f"{URL}/recipe/"

# Función para extraer recetas y categorias con parámetros
def extract_data(limit=0, skip=0, endpoint=ENDPOINT_RECIPES,filename="raw_data.json"):
    params = {
        "limit": str(limit),
        "skip": str(skip),
    }
    response = requests.post(endpoint, params=params)
    if response.status_code == 200:

        # Guardar raw data integro para usar después en la transformación
        data = response.json()
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("Datos extraídos y guardados en "+ filename)

    else:
        print("Error al obtener datos")
        return None

# Función para obtener el detalle de una receta específica
def extract_recipe_detail(recipe_name):
    response = requests.get(f"{ENDPOINT_RECIPE_DETAIL}{recipe_name}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener detalles de {recipe_name}")
        return None

#extract_data(50,0,ENDPOINT_CATEGORIES,"./json_data/raw_data_categories.json")
extract_data(0, 0, ENDPOINT_RECIPES, "json_data/raw_data_recipes.json")
