from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import joblib
import tensorflow as tf
from pydantic import BaseModel
from typing import Dict

# Cargar el modelo y transformadores
model = tf.keras.models.load_model("best_iot_model.h5")
scaler = joblib.load("scaler.pkl")
encoder = joblib.load("onehot_encoder.pkl")
features_to_keep = joblib.load("selected_features.pkl")

# FastAPI app
app = FastAPI()

# Permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir a ["http://localhost:3000"] si deseas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definir el esquema de entrada
class FeaturesInput(BaseModel):
    features: Dict[str, float]

@app.post("/predict")
def predict(data: FeaturesInput):
    try:
        # Convertir dict a vector con los features correctos
        feature_dict = data.features
        input_vector = np.array([[feature_dict.get(feat, 0.0) for feat in features_to_keep]])
        input_scaled = scaler.transform(input_vector)
        
        # Hacer predicción
        y_pred = model.predict(input_scaled)
        pred_index = np.argmax(y_pred)
        pred_label = encoder.categories_[0][pred_index]

        return {
            "predicted_class": pred_label,
            "confidence": float(np.max(y_pred)),
            "probabilities": {encoder.categories_[0][i]: float(prob) for i, prob in enumerate(y_pred[0])}
        }
    except Exception as e:
        return { "error": str(e) }
