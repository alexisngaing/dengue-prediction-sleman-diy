from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
from preprocess import preprocess_sleman, preprocess_kapanewon

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

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

if __name__ == '__main__':
    app.run(debug=True)
