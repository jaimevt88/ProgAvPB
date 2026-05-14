from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import joblib
import os
import time

# ----------------------------------------
# esperar PostgreSQL
# ----------------------------------------

time.sleep(5)

# ----------------------------------------
# conexión DB
# ----------------------------------------

DATABASE_URL = "postgresql://mluser:mlpass@postgres:5432/mldb"

engine = create_engine(DATABASE_URL)

# ----------------------------------------
# leer dataset desde PostgreSQL
# ----------------------------------------

df = pd.read_sql(
    "SELECT * FROM iris_dataset",
    engine
)

print("\nDataset cargado desde PostgreSQL\n")

print(df.head())

# ----------------------------------------
# separar features y target
# ----------------------------------------

X = df.drop("target", axis=1)

y = df["target"]

# ----------------------------------------
# dividir dataset
# ----------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ----------------------------------------
# crear modelo
# ----------------------------------------

model = RandomForestClassifier()

# ----------------------------------------
# entrenar
# ----------------------------------------

model.fit(X_train, y_train)

# ----------------------------------------
# evaluar
# ----------------------------------------

accuracy = model.score(X_test, y_test)

print(f"\nAccuracy: {accuracy}\n")

# ----------------------------------------
# guardar modelo
# ----------------------------------------

os.makedirs("/models", exist_ok=True)

joblib.dump(model, "/models/model.pkl")

print("Modelo guardado en /models/model.pkl")

# ----------------------------------------
# guardar metadata
# ----------------------------------------

metadata = pd.DataFrame([{
    "model_name": "RandomForest",
    "accuracy": accuracy
}])

metadata.to_sql(
    "models",
    engine,
    if_exists="append",
    index=False
)

print("Metadata almacenada en PostgreSQL")
