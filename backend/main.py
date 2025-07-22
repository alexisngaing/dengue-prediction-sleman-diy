from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os

app = Flask(__name__)
CORS(app)

# Load models
model_kabupaten = joblib.load("model_kabupaten.pkl")
model_kecamatan = joblib.load("model_kecamatan.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    csv_file = request.files['file']
    model_type = request.form.get('model_type', 'kabupaten')

    try:
        df = pd.read_csv(csv_file)

        # Validasi kolom
        required_columns = ['date', 'temperature_avg_celsius', 'humidity_avg_percentage', 'precipitation_mm']
        if model_type == 'kecamatan':
            required_columns.insert(1, 'sub_district')  # Tambahkan sub_district

        if not all(col in df.columns for col in required_columns):
            return jsonify({"error": "Missing required columns"}), 400

        # Pilih model
        model = model_kabupaten if model_type == 'kabupaten' else model_kecamatan

        # Ambil fitur yang sesuai untuk prediksi
        features = df[['temperature_avg_celsius', 'humidity_avg_percentage', 'precipitation_mm']]
        prediction = model.predict(features)

        # Gabungkan hasil prediksi
        df['predicted_cases'] = prediction

        # Pilih kolom yang akan dikirim kembali ke frontend
        response_columns = required_columns + ['predicted_cases']
        result = df[response_columns].to_dict(orient='records')

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
