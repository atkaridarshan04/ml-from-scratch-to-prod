from sklearn.impute import SimpleImputer
import pandas as pd

def fit_median_imputer(df: pd.DataFrame, column: str) -> SimpleImputer:
    # Fit a median SimpleImputer on a single column
    imputer = SimpleImputer(strategy='median')
    imputer.fit(df[[column]])
    return imputer

def apply_imputer_transformation(df: pd.DataFrame, column: str, imputer: SimpleImputer) -> pd.DataFrame:
    # Apply a fitted imputer to a dataframe column.
    df = df.copy()
    df[column] = imputer.transform(df[[column]])
    return df