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

# Consultar datos de relación dificultad y tiempo de coccion
query = "SELECT difficulty, cook_time FROM recipes"
df_diff = pd.read_sql(query, engine)

# Crear boxplot
plt.figure(figsize=(8, 6))
sns.boxplot(x=df_diff["difficulty"], y=df_diff["cook_time"])

plt.xlabel("Dificultad")
plt.ylabel("Tiempo de Cocción (min)")
plt.title("Dificultad vs. Tiempo de Cocción")

plt.show()
