import pandas as pd
import numpy as np

def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    # Add domain-specific engineered features.
    df = df.copy()

    # Avoid division by zero
    df["rooms_per_household"] = df["total_rooms"] / df["households"].replace(0, np.nan)
    df["bedrooms_per_room"] = df["total_bedrooms"] / df["total_rooms"].replace(0, np.nan)
    df["population_per_household"] = df["population"] / df["households"].replace(0, np.nan)

    return df
