from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
from preprocess import preprocess_sleman, preprocess_kapanewon
from flask_sqlalchemy import SQLAlchemy
from database import db
from models import Prediction
from datetime import datetime
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Buat database dan tabel jika belum ada
with app.app_context():
    db.create_all()

# Load models
sleman_model = joblib.load('models/xgb_model_sleman.pkl')
kapanewon_model = joblib.load('models/xgb_model_kapanewon.pkl')

# Feature list
sleman_features = [
    'temperature_min_celsius', 'humidity_avg_percentage', 'precipitation_mm',
    'case_lag1', 'case_lag2', 'case_lag3',
    'temperature_min_celsius_lag1', 'temperature_min_celsius_lag2', 'temperature_min_celsius_lag3',
    'humidity_avg_percentage_lag1', 'humidity_avg_percentage_lag2', 'humidity_avg_percentage_lag3',
    'precipitation_mm_lag1', 'precipitation_mm_lag2', 'precipitation_mm_lag3',
    'case_rolling3', 
    'temperature_min_celsius_rolling3',
    'humidity_avg_percentage_rolling3', 'precipitation_mm_rolling3',
    'month', 'season'
]

kapanewon_features = sleman_features + ['sub_district_encoded']

POPULATION_SLEMAN = 1125804
POPULATION_KAPANEWON = {
    'gamping': 93549,
    'godean': 69949,
    'moyudan': 33676,
    'minggir': 32585,
    'seyegan': 50965,
    'mlati': 92083,
    'depok': 122305,
    'berbah': 54789,
    'prambanan': 53948,
    'kalasan': 82267,
    'ngemplak': 62437,
    'ngaglik': 96996,
    'sleman': 69510,
    'tempel': 54345,
    'turi': 37274,
    'pakem': 37588,
    'cangkringan': 31309,
}

@app.route('/predict/sleman', methods=['POST'])
def predict_sleman():
    file = request.files['file']
    df = pd.read_csv(file)
    df = preprocess_sleman(df)

    print("After preprocessing:", df.shape)
    print("Kolom tersedia:", df.columns.tolist())

    if df.empty:
        print("⚠️ Data kosong setelah preprocessing")
        return jsonify([])

    X = df[sleman_features]
    df['predicted_cases'] = sleman_model.predict(X)
    result = df[['date', 'temperature_min_celsius', 'humidity_avg_percentage', 'precipitation_mm', 'predicted_cases']].to_dict(orient='records')
    return jsonify(result)

@app.route('/predict/kapanewon', methods=['POST'])
def predict_kapanewon():
    file = request.files['file']
    df = pd.read_csv(file)
    df = preprocess_kapanewon(df)
    X = df[kapanewon_features]
    df['predicted_cases'] = kapanewon_model.predict(X)
    result = df[['date', 'sub_district', 'temperature_min_celsius', 'humidity_avg_percentage', 'precipitation_mm', 'predicted_cases']].to_dict(orient='records')
    return jsonify(result)

@app.route('/save_prediction', methods=['POST'])
def save_prediction():
    data = request.json  # frontend kirim array of prediksi
    model_type = request.args.get('model_type', 'sleman')

    for row in data:
        # Ambil populasi sesuai model_type
        if model_type == 'sleman':
            population = POPULATION_SLEMAN
            multiplier = 100_000
        else:
            sub_district = row.get('sub_district')
            population = POPULATION_KAPANEWON.get(sub_district, 1)  # Default 1 untuk hindari zero division
            multiplier = 10_000

        incidence = (row['predicted_cases'] / population) * multiplier

        pred = Prediction(
            date=datetime.strptime(row['date'], '%Y-%m-%d').date(),
            temperature_min_celsius=row['temperature_min_celsius'],
            humidity_avg_percentage=row['humidity_avg_percentage'],
            precipitation_mm=row['precipitation_mm'],
            predicted_cases=row['predicted_cases'],
            incidence_rate=incidence,
            sub_district=row.get('sub_district', None),
            model_type=model_type
        )
        db.session.add(pred)
    db.session.commit()
    return jsonify({'message': 'Hasil prediksi berhasil disimpan.'}), 201

@app.route('/all-predictions', methods=['GET'])
def get_all_predictions():
    predictions = Prediction.query.order_by(Prediction.date.asc()).all()
    result = [
        {
            'date': p.date,
            'predicted_cases': p.predicted_cases,
            'incidence_rate': p.incidence_rate,
        }
        for p in predictions
    ]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
