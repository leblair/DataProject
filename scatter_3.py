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

# Recetas por categoria
query = "SELECT category_id, COUNT(*) as total FROM recipes GROUP BY category_id;"
df_cat = pd.read_sql(query, engine)

# Crear gráfico de barras
plt.figure(figsize=(12, 6))
sns.barplot(x=df_cat["total"], y=df_cat["category_id"], palette="viridis")

plt.xlabel("Número de Recetas")
plt.ylabel("Categoría")
plt.title("Número de Recetas por Categoría")

plt.show()
