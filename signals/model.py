# signals/model.py

import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from joblib import dump

def create_target(df: pd.DataFrame, price_increase_pct: float = 0.03, lookahead_candles: int = 15) -> pd.Series:
    """
    Creates the target variable for the model.

    A buy signal (1) is generated if the 'High' price increases by a certain
    percentage within a given number of future candles.

    Args:
        df: The input DataFrame with stock data.
        price_increase_pct: The target percentage increase.
        lookahead_candles: The number of future candles to look at.

    Returns:
        A pandas Series representing the target variable.
    """
    df['future_high'] = df['High'].rolling(window=lookahead_candles).max().shift(-lookahead_candles)
    target = np.where(df['future_high'] >= df['Close'] * (1 + price_increase_pct), 1, 0)
    return pd.Series(target, index=df.index)

def train_model(df: pd.DataFrame, model_path: str):
    """
    Trains a LightGBM model and saves it to a file.

    Args:
        df: The DataFrame with features and target.
        model_path: The path to save the trained model.
    """
    # Define features (X) and target (y)
    features = df.select_dtypes(include=np.number).columns.tolist()
    features.remove('Close')
    features.remove('High')
    if 'future_high' in df.columns:
        features.remove('future_high')


    X = df[features]
    y = create_target(df)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Initialize and train the LightGBM classifier
    lgbm = lgb.LGBMClassifier(objective='binary', random_state=42)
    lgbm.fit(X_train, y_train)

    # Save the trained model
    dump(lgbm, model_path)
    print(f"Model trained and saved to {model_path}")

    # Evaluate the model (optional)
    accuracy = lgbm.score(X_test, y_test)
    print(f"Model accuracy on test set: {accuracy:.2f}")

def predict_signals(df: pd.DataFrame, model) -> np.ndarray:
    """
    Generates buy signals using a trained model.

    Args:
        df: The DataFrame with features.
        model: The trained LightGBM model.

    Returns:
        An array of predictions (0 or 1).
    """
    features = df.select_dtypes(include=np.number).columns.tolist()
    features.remove('Close')
    features.remove('High')

    X = df[features]
    return model.predict(X)

