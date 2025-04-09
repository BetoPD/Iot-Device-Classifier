import pandas as pd
import joblib
import json
import os

# Archivos necesarios
data_file = "iot_device_train.csv"
features_file = "selected_features.pkl"
output_dir = "real_test_json_by_class"

# Crear carpeta de salida
os.makedirs(output_dir, exist_ok=True)

# Cargar dataset y features
df = pd.read_csv(data_file)
features = joblib.load(features_file)

# Eliminar features que no estén en el dataset
features = [f for f in features if f in df.columns]

# Iterar por cada categoría real
for category in df["device_category"].unique():
    df_filtered = df[df["device_category"] == category]
    sample_row = df_filtered.sample(n=1, random_state=42)
    sample_dict = sample_row[features].to_dict(orient="records")[0]

    file_name = category.replace(" ", "_").lower() + ".json"
    output_path = os.path.join(output_dir, file_name)

    with open(output_path, "w") as f:
        json.dump(sample_dict, f, indent=2)

    print(f"✅ Generado: {output_path}")
