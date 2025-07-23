import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocess_sleman(df):
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['season'] = (df['month'] % 12) // 3 + 1

    # Buat salinan dari df untuk reference rolling dan lag
    df_ref = df.copy()

    # Hitung rolling dan lag dari data sebelumnya (dengan nilai case)
    lags = [1, 2, 3]
    for lag in lags:
        df[f'case_lag{lag}'] = df_ref['case'].shift(lag)
        df[f'temperature_min_celsius_lag{lag}'] = df_ref['temperature_min_celsius'].shift(lag)
        df[f'humidity_avg_percentage_lag{lag}'] = df_ref['humidity_avg_percentage'].shift(lag)
        df[f'precipitation_mm_lag{lag}'] = df_ref['precipitation_mm'].shift(lag)

    df['case_rolling3'] = df_ref['case'].rolling(window=3).mean()
    df['temperature_min_celsius_rolling3'] = df_ref['temperature_min_celsius'].rolling(window=3).mean()
    df['humidity_avg_percentage_rolling3'] = df_ref['humidity_avg_percentage'].rolling(window=3).mean()
    df['precipitation_mm_rolling3'] = df_ref['precipitation_mm'].rolling(window=3).mean()

    # Drop NaN, tapi jangan drop baris yang hanya NaN di kolom 'case'
    df = df[df['case_lag1'].notna()].reset_index(drop=True)

    return df

def preprocess_kapanewon(df):
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['season'] = (df['month'] % 12) // 3 + 1

    lag_features = ['case', 'temperature_min_celsius', 'humidity_avg_percentage', 'precipitation_mm']
    for feature in lag_features:
        for lag in [1, 2, 3]:
            df[f'{feature}_lag{lag}'] = df.groupby('sub_district')[feature].shift(lag)

    for col in lag_features:
        df[f'{col}_rolling3'] = df.groupby('sub_district')[col].transform(lambda x: x.rolling(window=3).mean())

    df = df.dropna().reset_index(drop=True)

    le = LabelEncoder()
    df['sub_district_encoded'] = le.fit_transform(df['sub_district'])

    return df
