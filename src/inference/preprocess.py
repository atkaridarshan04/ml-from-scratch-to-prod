from preprocessing import (
    apply_imputer_transformation,
    apply_one_hot_encoder,
    add_engineered_features
)
import pandas as pd

def preprocess_input(df: pd.DataFrame, artifacts: list) -> pd.DataFrame :
    # Apply preprocessing steps for inference.

    # Imputation
    df = apply_imputer_transformation(df, 'total_bedrooms', artifacts['imputer'])

    # Encoding
    df = apply_one_hot_encoder(df, 'ocean_proximity', artifacts['encoder'])

    # feature enginnering
    df = add_engineered_features(df)

    return df