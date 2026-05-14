import streamlit as st
import requests
import pandas as pd

# ----------------------------------------
# título
# ----------------------------------------

st.title("Iris ML Pipeline")

st.write(
    "Demo de pipeline de Machine Learning "
    "basado en Docker y FastAPI"
)

# ----------------------------------------
# sliders
# ----------------------------------------

sepal_length = st.slider(
    "Sepal Length",
    4.0,
    8.0,
    5.1
)

sepal_width = st.slider(
    "Sepal Width",
    2.0,
    5.0,
    3.5
)

petal_length = st.slider(
    "Petal Length",
    1.0,
    7.0,
    1.4
)

petal_width = st.slider(
    "Petal Width",
    0.1,
    3.0,
    0.2
)

# ----------------------------------------
# botón
# ----------------------------------------

if st.button("Predict"):

    payload = {
        "sepal_length": sepal_length,
        "sepal_width": sepal_width,
        "petal_length": petal_length,
        "petal_width": petal_width
    }

    response = requests.post(
        "http://api:8000/predict",
        json=payload
    )

    result = response.json()

    # ----------------------------------------
    # mostrar resultado
    # ----------------------------------------

    st.subheader("Prediction")

    classes = {
        0: "Setosa",
        1: "Versicolor",
        2: "Virginica"
    }

    prediction_name = classes[result["prediction"]]

    st.success(
        f"Predicción: {prediction_name}"
    )

    # ----------------------------------------
    # probabilidades
    # ----------------------------------------

    st.subheader("Probabilities")

    probabilities = pd.DataFrame({
        "Class": [
            "Setosa",
            "Versicolor",
            "Virginica"
        ],
        "Probability": result["probabilities"]
    })

    st.dataframe(probabilities)
