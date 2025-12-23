import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor

def fit_hgb_model(X_train: pd.DataFrame, y_train: pd.DataFrame, params: dict) -> HistGradientBoostingRegressor:
    hgb = HistGradientBoostingRegressor(**params)
    hgb.fit(X_train, y_train)
    return hgb