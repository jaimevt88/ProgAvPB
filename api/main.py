from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import time

# ----------------------------------------
# esperar modelo y postgres
# ----------------------------------------

time.sleep(5)

# ----------------------------------------
# cargar modelo
# ----------------------------------------

model = joblib.load("/models/model.pkl")

print("Modelo cargado")

# ----------------------------------------
# conexión DB
# ----------------------------------------

DATABASE_URL = "postgresql://mluser:mlpass@postgres:5432/mldb"

engine = create_engine(DATABASE_URL)

# ----------------------------------------
# crear app
# ----------------------------------------

app = FastAPI()

# ----------------------------------------
# esquema request
# ----------------------------------------

class IrisRequest(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# ----------------------------------------
# endpoint raíz
# ----------------------------------------

@app.get("/")
def root():
    return {
        "message": "Iris ML API funcionando"
    }

# ----------------------------------------
# endpoint predict
# ----------------------------------------

@app.post("/predict")
def predict(data: IrisRequest):

    features = np.array([[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]])

    prediction = model.predict(features)[0]

    probabilities = model.predict_proba(features)[0]

    result = {
        "prediction": int(prediction),
        "probabilities": probabilities.tolist()
    }

    # ----------------------------------------
    # guardar predicción
    # ----------------------------------------

    prediction_df = pd.DataFrame([{
        "sepal_length": data.sepal_length,
        "sepal_width": data.sepal_width,
        "petal_length": data.petal_length,
        "petal_width": data.petal_width,
        "prediction": int(prediction)
    }])

    prediction_df.to_sql(
        "predictions",
        engine,
        if_exists="append",
        index=False
    )

    return result
