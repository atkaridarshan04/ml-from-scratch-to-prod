from sklearn.metrics import r2_score, root_mean_squared_error

def evaluate_regression(y_true, y_pred) -> dict:
    return {
        "rmse": root_mean_squared_error(y_true, y_pred),
        "r2": r2_score(y_true, y_pred)
    }