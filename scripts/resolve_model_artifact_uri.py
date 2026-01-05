from mlflow.tracking import MlflowClient

client = MlflowClient()

model_name = "CaliforniaHousingRegressor"
alias = "production"

mv = client.get_model_version_by_alias(
    name=model_name,
    alias=alias
)

download_uri = client.get_model_version_download_uri(
    name=model_name,
    version=mv.version
)

print("Resolved artifact URI:", download_uri)