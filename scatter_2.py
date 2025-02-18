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

# Consultar recetas con más ingredientes
query = "SELECT recipe_id, num_ingredients FROM recipes ORDER BY num_ingredients DESC LIMIT 10"
df_ingredients = pd.read_sql(query, engine)

# Crear gráfico de barras
plt.figure(figsize=(10, 5))
sns.barplot(x=df_ingredients["num_ingredients"], y=df_ingredients["recipe_id"], palette="coolwarm")

plt.xlabel("Número de Ingredientes")
plt.ylabel("Receta")
plt.title("Top 10 Recetas con Más Ingredientes")

plt.show()
