import pandas as pd
from sklearn.preprocessing import StandardScaler

def fit_standard_scaler(df: pd.DataFrame, colums: list) -> StandardScaler:
    # Fit StandardScaler on numeric columns using training data.
    scalar = StandardScaler()
    scalar.fit(df[colums])
    return scalar

def apply_standard_scaler(df: pd.DataFrame, columns: list, scalar: StandardScaler) -> pd.DataFrame:
    df = df.copy()
    df[columns] = scalar.transform(df[columns])
    return df