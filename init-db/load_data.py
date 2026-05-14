import pandas as pd
from sqlalchemy import create_engine
import time

# ----------------------------------------
# esperar postgres
# ----------------------------------------

time.sleep(5)

# ----------------------------------------
# conexión PostgreSQL
# ----------------------------------------

DATABASE_URL = "postgresql://mluser:mlpass@postgres:5432/mldb"

engine = create_engine(DATABASE_URL)

# ----------------------------------------
# leer CSV
# ----------------------------------------

df = pd.read_csv("/datasets/iris.csv")

print("Dataset cargado desde CSV")

print(df.head())

# ----------------------------------------
# cargar en PostgreSQL
# ----------------------------------------

df.to_sql(
    "iris_dataset",
    engine,
    if_exists="replace",
    index=False
)

print("Tabla iris_dataset creada")

print(f"Registros insertados: {len(df)}")
