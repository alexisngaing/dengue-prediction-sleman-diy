from database import db

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    temperature_min_celsius = db.Column(db.Float, nullable=False)
    humidity_avg_percentage = db.Column(db.Float, nullable=False)
    precipitation_mm = db.Column(db.Float, nullable=False)
    predicted_cases = db.Column(db.Float, nullable=False)
    incidence_rate = db.Column(db.Float, nullable=True) 
    sub_district = db.Column(db.String, nullable=True)  # opsional untuk model kapanewon
    model_type = db.Column(db.String, nullable=False)   # 'sleman' atau 'kapanewon'
