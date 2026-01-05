import pandas as pd
import mlflow.pyfunc

from src.preprocessing.imputation import apply_imputer_transformation
from src.preprocessing.encoding import apply_one_hot_encoder
from src.preprocessing.feature_engineering import add_engineered_features

class HousingInferencePipeline(mlflow.pyfunc.PythonModel):
    """
    Single deployable inference pipeline:
    preprocessing + model
    """

    def __init__(self, imputer, encoder, model):
        self.imputer = imputer
        self.encoder = encoder
        self.model = model

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        df = apply_imputer_transformation(df, "total_bedrooms", self.imputer)
        df = apply_one_hot_encoder(df, "ocean_proximity", self.encoder)
        df = add_engineered_features(df)
        return df

    def predict(self, context, model_input: pd.DataFrame, params=None):
        X = self.preprocess(model_input)
        return self.model.predict(X)
