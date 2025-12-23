import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def fit_one_hot_encoder(df: pd.DataFrame, column: str) -> OneHotEncoder:
    # Fit OneHotEncoder on a single categorical column.
    ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    ohe.fit(df[[column]])
    return ohe

def apply_one_hot_encoder(df: pd.DataFrame, column: str, ohe: OneHotEncoder) -> pd.DataFrame:
    # Apply a fitted OneHotEncoder and return dataframe with original column replaced by encoded columns.
    df = df.copy()

    encoded_array = ohe.transform(df[[column]])
    encoded_cols = ohe.get_feature_names_out()

    encoded_df = pd.DataFrame(encoded_array, columns=encoded_cols, index=df.index)

    df = df.drop(columns=[column])
    df = df.join(encoded_df)

    return df