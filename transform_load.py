import pandas as pd
import json
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()  #load env file
DB_USER=os.getenv('DB_USER')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_HOST=os.getenv('DB_HOST')
DB_NAME=os.getenv('DB_NAME')

# Crear conexión con SQLAlchemy
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

#Funcion para cargar DataFrame en MySQL
def load_data_to_mysql(df, table_name,mode):
    try:
        df.to_sql(table_name, con=engine, if_exists=mode, index=False)
        print("Datos insertados correctamente en MySQL.")
    except Exception as e:
        print(f"Error al insertar datos: {e}")

#Funcion para crear Dataframe a partir de raw_data
def transform_recipe_data():
    print("Leyendo recetas a procesar...")
    with open('json_data/raw_data_recipes.json', 'r', encoding="latin_1") as file:
        data = json.load(file)

    processed_recipes = []

    #Añadir campos como niceName, difficulty, cookingTime, ingredients, etc.).
    for recipe in data.get("result", []):
        # Calculo de promedio de ratings de receta
        ratings = recipe.get("ratings", [])
        avg_rating = sum(r["rate"] for r in ratings if "rate" in r) / len(ratings) if ratings else None
        #Valor calorico de receta
        energy_info = recipe.get("nutritional", {}).get("Energy", {})
        energy_value = energy_info.get("value", 0)

        processed_recipes.append({
            "recipe_id": recipe.get("niceName", "N/A"),
            "description": recipe.get("title", "N/A").encode("latin_1"),
            "difficulty": recipe.get("difficulty","N/A"),
            "cook_time": round(int(recipe.get("cookTime",0))/60), #pasar a minutos
            "category_id": recipe.get("categoryNiceName", "N/A"),
            "num_ingredients": len(recipe.get("ingredients", [])),
            "price": recipe.get("price", "N/A"),
            "rating": round(avg_rating, 2) if avg_rating else None,
            "calories": round(energy_value, 2) if energy_value else None,
        })


    data_frame = pd.DataFrame(processed_recipes)
    dfresult = data_frame.dropna(subset=['recipe_id']) #quita las recetas sin id
    dfresult = dfresult.drop_duplicates(subset=['recipe_id']) #quita las recetas duplicadas
    return dfresult


#Funcion para crear Dataframe a partir de raw_data de categories.
def transform_categories_data():
    #Leer raw data
    print("Leyendo categorias a procesar...")

    with open('json_data/raw_data_categories.json', 'r', encoding="latin_1") as file:
        data = json.load(file)

    processed_categories = []

    #Añadir campos
    for category in data:
        processed_categories.append({
                "category_id": category.get("niceName", "N/A"),
                "description": category.get("name","N/A").encode("latin_1"),
                "count": category.get("count","N/A"),
            })
    #Categoria inexistente en categorias pero sí en recipes > añadir manualmente para referencia en db:
    processed_categories.append({"category_id": "otras","description":"N/A", "count": "N/A"})
    processed_categories.append({"category_id": "funciones","description":"N/A", "count": "N/A"})
    data_frame = pd.DataFrame(processed_categories)

    dfresult = data_frame.dropna(subset=['category_id']) #quita las categories sin id
    dfresult= dfresult.drop_duplicates(subset=['category_id']) #quita las categorias duplicadas

    return dfresult



#Dataframes
df_categories = transform_categories_data()
df_recipes = transform_recipe_data()

#Hacer files csv
df_recipes.to_csv("./csv_files/processed_recipes.csv", index=False, encoding='utf-8')
df_categories.to_csv("./csv_files/processed_categories.csv", index=False, encoding='utf-8')

#Cargar Dataframe a database
#load_data_to_mysql(df_categories,"categories","append")
load_data_to_mysql(df_recipes,"recipes","append")

