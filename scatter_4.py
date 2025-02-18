import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()  #load env file
# Conectar a la base de datos
DB_URI = os.getenv('DB_URI')
engine = create_engine(DB_URI)

# Query para obtener recetas rápidas y bajas en calorías
query = "SELECT recipe_id, cook_time, calories FROM recipes WHERE cook_time != 0 and cook_time <= 15 AND calories <= 500 order by cook_time, calories asc limit 10;"
df = pd.read_sql(query, engine)


# Crear el gráfico de barras
plt.figure(figsize=(10, 6))
plt.bar(df["recipe_id"], df["calories"], color="skyblue", alpha=0.7)
plt.xticks(rotation=90)

# Etiquetas y título
plt.xlabel("Recetas")
plt.ylabel("Calorías")
plt.title("Top 10 recetas rápidas y bajas en calorías")
plt.grid(axis="y", linestyle="--", alpha=0.7)

plt.show()