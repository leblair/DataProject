import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()  #load env file
# Conectar a la base de datos
DB_URI = os.getenv('DB_URI')
engine = create_engine(DB_URI)

# Consultar tiempo de coccion recetas
query = "SELECT cook_time FROM recipes where cook_time<=150;"
df = pd.read_sql(query, engine)

# Crear el histograma con Pandas
df["cook_time"].plot(kind="hist", bins=np.arange(0, df["cook_time"].max()+10, 10),
                     color="green", edgecolor="black", alpha=0.7)

# Configurar etiquetas
plt.xlabel("Tiempo de cocción (min)")
plt.ylabel("Número de recetas")
plt.title("Distribución de tiempos de cocción")

# Mostrar el gráfico
plt.show()
