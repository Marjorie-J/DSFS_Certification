import argparse
import pandas as pd
import time
import mlflow
from mlflow.models.signature import infer_signature
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import  StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline


if __name__ == "__main__":

    # Set your variables for your environment
    EXPERIMENT_NAME = "getaround_pricing"

    # Set tracking URI to your Heroku application
    mlflow.set_tracking_uri("https://marjg-getaround-mlflow.hf.space/")

    # Set experiment's info
    mlflow.set_experiment(EXPERIMENT_NAME)

    # Get our experiment info
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)


    print("training model...")

    # Time execution
    start_time = time.time()

    # Call mlflow autolog
    mlflow.sklearn.autolog(log_models=False)  # We won't log models right away

    # Parse arguments given in shell script
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_estimators", default=1)
    parser.add_argument("--min_samples_split", default=2)
    args = parser.parse_args()

    # Import dataset
    df = pd.read_csv("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv", index_col=0)

    # X, y split 
    target = "rental_price_per_day"

    X = df.drop(target, axis=1)
    y = df[target]

    # Train / test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Preprocessing
    categorical_features = X_train.select_dtypes(include=["bool", "object"]).columns

    categorical_transformer = OneHotEncoder(
        drop="first", handle_unknown="error", sparse_output=False
    )

    numerical_features = X_train.select_dtypes(include=["int", "float"]).columns
    
    numerical_transformer = StandardScaler()

    feature_preprocessor = ColumnTransformer(
        transformers=[
            ("categorical_transformer", categorical_transformer, categorical_features),
            ("numerical_transformer", numerical_transformer, numerical_features),
        ]
    )

    # Pipeline
    n_estimators = int(args.n_estimators)
    min_samples_split = int(args.min_samples_split)

    model = Pipeline(
        steps=[
            ("features_preprocessing", feature_preprocessor),
            ("Regressor", RandomForestRegressor(n_estimators=n_estimators, min_samples_split=min_samples_split, random_state=42))
        ]
    )

    # Log experiment to MLFlow
    with mlflow.start_run(experiment_id=experiment.experiment_id) as run:
        model.fit(X_train, y_train)
        predictions = model.predict(X_train)

        # Log model seperately to have more flexibility on setup
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="getaround_pricing_optimization",
            registered_model_name="getaround_pricing_optimization_RF",
            signature=infer_signature(X_train, predictions),
        )

    print("...Done!")
    print(f"---Total training time: {time.time()-start_time}")