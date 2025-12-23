# Take a small sample WITHOUT target
import pandas as pd

df = pd.read_csv("data/raw/housing.csv")

sample = df.drop(columns=["median_house_value"]).sample(10, random_state=42)

sample.to_csv("data/inference/sample_input.csv", index=False)