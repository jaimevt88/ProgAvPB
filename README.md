# Iris ML Pipeline — Docker + FastAPI + Streamlit

## Descripción

Este proyecto implementa un pipeline completo de Machine Learning basado en microservicios utilizando Docker.

La solución integra:

* PostgreSQL para persistencia
* FastAPI para inferencia
* Streamlit para frontend
* Scikit-learn para entrenamiento ML
* Docker Compose para orquestación

El sistema permite:

1. Cargar un dataset CSV en PostgreSQL
2. Entrenar un modelo de Machine Learning
3. Guardar el modelo entrenado
4. Exponer un endpoint REST para predicciones
5. Consumir la API desde un frontend web
6. Persistir predicciones realizadas

---

# Arquitectura

```text
Usuario
   ↓
Frontend Streamlit
   ↓
FastAPI API
   ↓
Modelo ML (.pkl)
   ↑
Training Container
   ↓
PostgreSQL
   ↑
Init-DB Container
   ↑
iris.csv
```

---

# Tecnologías utilizadas

| Componente           | Tecnología     |
| -------------------- | -------------- |
| Frontend             | Streamlit      |
| API REST             | FastAPI        |
| ML                   | Scikit-learn   |
| Base de datos        | PostgreSQL     |
| Contenedores         | Docker         |
| Orquestación         | Docker Compose |
| Persistencia modelos | Joblib         |

---

# Estructura del proyecto

```text
iris-ml-pipeline/
│
├── .gitignore
├── docker-compose.yml
│
├── api/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
│
├── datasets/
│   └── iris.csv
│
├── db/
│
├── frontend/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── init-db/
│   ├── Dockerfile
│   ├── load_data.py
│   └── requirements.txt
│
├── models/
│
├── training/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── train.py
│
└── README.md
```

---

# Flujo del sistema

```text
CSV Dataset
    ↓
Init-DB
    ↓
PostgreSQL
    ↓
Training Service
    ↓
model.pkl
    ↓
FastAPI
    ↓
Streamlit
    ↓
Usuario
```

---

# Requisitos

Antes de ejecutar el proyecto asegúrese de tener instalado:

* Docker
* Docker Compose

Verificar instalación:

```bash
docker --version

docker compose version
```

---

# Ejecución paso a paso

# 1. Clonar repositorio

```bash
git clone <REPO_URL>

cd iris-ml-pipeline
```

---

# 2. Construir contenedores

```bash
docker compose build
```

---

# 3. Levantar PostgreSQL

```bash
docker compose up -d postgres
```

---

# 4. Cargar dataset en PostgreSQL

```bash
docker compose run init-db
```

Este paso:

* lee `iris.csv`
* crea la tabla `iris_dataset`
* inserta los registros en PostgreSQL

---

# 5. Ejecutar entrenamiento

```bash
docker compose run training
```

Este paso:

* carga datos desde PostgreSQL
* entrena RandomForest
* calcula accuracy
* genera `model.pkl`
* almacena metadata del modelo

---

# 6. Levantar API y frontend

```bash
docker compose up api frontend
```

---

# Servicios disponibles

| Servicio     | URL                                                      |
| ------------ | -------------------------------------------------------- |
| FastAPI      | [http://localhost:8000](http://localhost:8000)           |
| Swagger Docs | [http://localhost:8000/docs](http://localhost:8000/docs) |
| Streamlit    | [http://localhost:8501](http://localhost:8501)           |

---

# Probar API con curl

## Endpoint raíz

```bash
curl http://localhost:8000
```

Resultado esperado:

```json
{"message":"Iris ML API funcionando"}
```

---

## Predicción

```bash
curl -X POST http://localhost:8000/predict \
-H "Content-Type: application/json" \
-d '{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}'
```

Resultado esperado:

```json
{
  "prediction": 0,
  "probabilities": [
    1.0,
    0.0,
    0.0
  ]
}
```

---

# Verificar PostgreSQL

Entrar al contenedor:

```bash
docker exec -it postgres psql -U mluser -d mldb
```

---

# Consultas útiles

## Ver tablas

```sql
\dt
```

---

## Ver dataset

```sql
SELECT * FROM iris_dataset LIMIT 5;
```

---

## Ver metadata de modelos

```sql
SELECT * FROM models;
```

---

## Ver predicciones

```sql
SELECT * FROM predictions;
```

---

# Servicios del proyecto

# PostgreSQL

Responsable de:

* persistencia de datasets
* almacenamiento de metadatos
* almacenamiento de predicciones

---

# Init-DB

Responsable de:

* ingestión de datos
* ETL inicial
* carga del CSV en PostgreSQL

---

# Training

Responsable de:

* entrenamiento ML
* evaluación
* generación del modelo
* persistencia de metadatos

---

# API

Responsable de:

* serving ML
* inferencia online
* exposición REST
* almacenamiento de predicciones

---

# Frontend

Responsable de:

* interacción usuario-modelo
* visualización de resultados
* consumo de API

---



# Dataset utilizado

Se utiliza el conjunto de datos Iris de scikit-learn.

Dataset clásico de clasificación multiclase con:

* Setosa
* Versicolor
* Virginica

---
