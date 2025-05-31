import mlflow
import uvicorn
import json
import pandas as pd
from pydantic import BaseModel
from typing import Literal, List, Union
from fastapi import FastAPI, File, UploadFile

description = """
The GetAround API helps car owners optimize rental pricing through intelligent predictions, 
while also providing insights to better understand their vehicles and make informed decisions.

## Preview

Where you can: 
* `/preview` a few rows of your dataset
* get `/unique-values` of a given column in your dataset

## Categorical

Where you can: 
* `/groupby` a given column and chose an aggregation metric 
* `/filter-by` one of several categories within your dataset 

## Predictions

Where you can:
* `/predict` the optimum price for a car
* `/batch-predict` where you can upload a file to get predictions for several cars


Check out documentation for more information on each endpoint. 
"""

tags_metadata = [
    {
        "name": "Categorical",
        "description": "Endpoints that deal with categorical data",
    },
    {"name": "Preview", "description": "Endpoints that quickly explore dataset"},
    {
        "name": "Predictions",
        "description": "Endpoints that uses our Machine Learning model for pricing optimization",
    },
]

app = FastAPI(
    title="🚙 GETAROUND API",
    description=description,
    version="0.1",
    contact={
        "name": "GETAROUND API - by Marjorie Janda"
    },
    openapi_tags=tags_metadata,
)


class GroupBy(BaseModel):
    column: str
    by_method: Literal["mean", "median", "max", "min", "sum", "count"] = "mean"


class FilterBy(BaseModel):
    column: str
    by_category: List[str] = None


class PredictionFeatures(BaseModel):
    model_key: str
    mileage: Union[int, float]
    engine_power: Union[int, float]
    fuel: str
    paint_color: str
    car_type: str
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car : bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool


@app.get("/", tags=["Introduction Endpoints"])
async def index():
    """
    Simply returns a welcome message!
    """
    message = "Hello world! This `/` is the most simple and default endpoint. If you want to learn more, check out documentation of the api at `/docs` or first check `/preview`"
    return message


@app.get("/preview", tags=["Preview"])
async def preview(rows: int = 10):
    """
    Get a sample of your whole dataset.
    You can specify how many rows you want by specifying a value for `rows`, default is `10`
    """
    df = pd.read_csv("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv", index_col=0)
    sample = df.sample(rows)
    return sample.to_dict(orient="records")


@app.get("/unique-values", tags=["Preview"])
async def unique_values(column: str):
    """
    Get unique values from a given column
    """
    df = pd.read_csv("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv", index_col=0)
    unique_vals = df[column].dropna().unique().tolist()

    return unique_vals


@app.post("/groupby", tags=["Categorical"])
async def group_by(groupBy: GroupBy):
    """
    Get data grouped by a given column. Accepted columns are:

    * `["model_key","fuel", "paint_color", "car_type"]`

    You can use different method to group by category which are:

    * `mean`
    * `median`
    * `min`
    * `max`
    * `sum`
    * `count`
    """

    df = pd.read_csv("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv", index_col=0)

    method = groupBy.by_method

     # Ne garder que les colonnes numériques pour l'agrégation
    numeric_cols = df.select_dtypes(include=["float", "int"]).columns


    if method == "mean":
        df = df.groupby(groupBy.column)[numeric_cols].mean()
    if method == "median":
        df = df.groupby(groupBy.column)[numeric_cols].median()
    if method == "min":
        df = df.groupby(groupBy.column)[numeric_cols].min()
    if method == "max":
        df = df.groupby(groupBy.column)[numeric_cols].max()
    if method == "sum":
        df = df.groupby(groupBy.column)[numeric_cols].sum()
    if method == "count":
        df = df.groupby(groupBy.column)[numeric_cols].count()

    df = df.reset_index()
    return df.to_dict(orient="records")


@app.post("/filter-by", tags=["Categorical"])
async def filter_by(filterBy: FilterBy):
    """
    Filter by one or more categories in a given column. Columns possible values are:

    * `["model_key","fuel", "paint_color", "car_type"]`

    Check values within dataset to know what kind of `categories` you can filter by. You can use `/unique-values` path to check them out.
    `categories` must be `list` format.
    """

    df = pd.read_csv("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv", index_col=0)

    if filterBy.by_category != None:
        df = df[df[filterBy.column].isin(filterBy.by_category)]
        df = df.reset_index()
        return df.to_dict(orient="records")
    else:
        msg = "Please chose a column to filter by"
        return msg


@app.post("/predict", tags=["Predictions"])
async def predict(predictionFeatures: PredictionFeatures):
    """
    Prediction for one observation. Endpoint will return a dictionnary like this:

    ```
    {'prediction': PREDICTION_VALUE}
    ```

    You need to give this endpoint all columns values as dictionnary, or form data.
    """
    # Read data
    df = pd.DataFrame([predictionFeatures.dict()])
    # Log model from mlflow
    logged_model = "runs:/21ce144d259c49a6a7a7e28be3fccecb/getaround_pricing_optimization"

    # Load model as a PyFuncModel.
    loaded_model = mlflow.pyfunc.load_model(logged_model)

    # prediction = loaded_model.predict(df)
    prediction = loaded_model.predict(pd.DataFrame(df))

    # Format response
    response = {"prediction": prediction.tolist()[0]}
    return response


@app.post("/batch-predict", tags=["Predictions"])
async def batch_predict(file: UploadFile = File(...)):
    """
    Make prediction on a batch of observation. This endpoint accepts only **csv files** containing
    all the trained columns WITHOUT the target variable.
    """
    # Read file
    df = pd.read_csv(file.file)

    # Log model from mlflow
    logged_model = "runs:/21ce144d259c49a6a7a7e28be3fccecb/getaround_pricing_optimization"

    # Load model as a PyFuncModel.
    loaded_model = mlflow.pyfunc.load_model(logged_model)
    predictions = loaded_model.predict(pd.DataFrame(df))

    return predictions.tolist()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000, debug=True, reload=True)
