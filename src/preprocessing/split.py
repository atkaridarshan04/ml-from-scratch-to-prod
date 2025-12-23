from sklearn.model_selection import train_test_split
import pandas as pd

def split_features(df: pd.DataFrame, target_col: str):
    X = df.drop(columns=target_col, axis=1)
    y = df[target_col]
    return X, y

def train_test_split_data(X, y, test_size: float = 0.2, random_state: int = 42):
    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
    )