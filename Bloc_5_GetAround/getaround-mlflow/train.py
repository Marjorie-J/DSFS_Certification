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
from sklearn.impute import SimpleImputer


if __name__ == "__main__":

    ### MLFLOW Experiment setup
    experiment_name="getaround_pricing"
    mlflow.set_experiment(experiment_name)

    print("training model...")
    
    # Time execution
    start_time = time.time()

    # Log experiment to MLFlow
    with mlflow.start_run() as run:
        # Call mlflow autolog
        mlflow.sklearn.autolog(log_models=False) # We won't log models right away

        # Parse arguments given in shell script
        parser = argparse.ArgumentParser()
        parser.add_argument("--n_estimators")
        parser.add_argument("--min_samples_split")
        args = parser.parse_args()

        # Import dataset
        df = pd.read_csv("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv", index_col=0)

        # X, y split 
        target = "rental_price_per_day"

        x = df.drop(target, axis=1)
        y = df[target]

        # Train / test split 
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


        # Preprocessing 
        numerical_columns = x_train.select_dtypes(include=["int", "float"]).columns
        categorical_columns = x_train.select_dtypes(include=["bool", "object"]).columns
        
        numeric_transformer = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="mean")),
            ("scaler", StandardScaler())
        ])

        categorical_transformer = Pipeline(
            steps=[
            ("encoder", OneHotEncoder(drop="first", handle_unknown="ignore"))
            ])

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, numerical_columns),
                ("cat", categorical_transformer, categorical_columns)
            ])

        x_train = preprocessor.fit_transform(x_train)
        x_test = preprocessor.transform(x_test) 

        # Pipeline 
        n_estimators = int(args.n_estimators)
        min_samples_split=int(args.min_samples_split)

        # Random Forest
        rfc = RandomForestRegressor(n_estimators=n_estimators, min_samples_split=min_samples_split, random_state=42)


        rfc.fit(x_train, y_train)
        predictions = rfc.predict(x_train)

        # Log model seperately to have more flexibility on setup 
        mlflow.sklearn.log_model(
            sk_model=rfc,
            artifact_path="getaround_pricing_optimization",
            registered_model_name="getaround_pricing_optimization_RF",
            signature=infer_signature(x_train, predictions)
        )
        
    print("...Done!")
    print(f"---Total training time: {time.time()-start_time}")