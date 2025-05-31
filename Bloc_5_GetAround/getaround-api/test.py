import requests
import json
import pandas as pd


### Test preview endpoint
def test_preview():
    print("###test_preview###")

    r = requests.get("https://marjg-getaround-api.hf.space/preview")

    response = r.json()
    print(pd.DataFrame(response))

test_preview()


### Test uniquevalues endpoint
def test_uniquevalues():
    print("###test_uniquevalues###")

    payload = {"column": "model_key"}
    r = requests.get("https://marjg-getaround-api.hf.space/unique-values", params=payload)

    response = r.json()
    print(response)

test_uniquevalues()


### Test groupby endpoint
def test_groupby():
    print("###test_groupby###")

    payload = {"column": "model_key", "by_method": "mean"}
    r = requests.post("https://marjg-getaround-api.hf.space/groupby", json=payload)

    response = r.json()
    print(pd.DataFrame(response))

test_groupby()


### Test filter-by endpoint
def test_filterBy():
    print("###test_filterBy###")

    payload = {
        "column": "paint_color",
        "by_category": ["black", "grey"],
    }

    r = requests.post("https://marjg-getaround-api.hf.space/filter-by", json=payload)

    response = r.json()
    print(pd.DataFrame(response))

test_filterBy()


#### Test ML Model
def test_prediction():
    print("###test_prediction###")

    payload = {
        "model_key": "Peugeot",
        "mileage": 139000,
        "engine_power": 135,
        "fuel": "diesel", 
        "paint_color": "blue",
        "car_type": "convertible",
        "private_parking_available": True,
        "has_gps": True,
        "has_air_conditioning": True,
        "automatic_car": True,
        "has_getaround_connect": True,
        "has_speed_regulator": True,
        "winter_tires": True
    }

    r = requests.post("https://marjg-getaround-api.hf.space/predict", json=payload)

    response = r.json()
    print(round(response["prediction"], 2))
    
test_prediction()


#### Test batch pred
def test_batch():
    print("###test_batchprediction###")

    df = pd.read_csv("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv", index_col=0)

    df = df.iloc[:, :-1]
    myfile = df.to_csv(index=False)
    r = requests.post("https://marjg-getaround-api.hf.space/batch-predict", files={"file": myfile})

    response = r.json()
    print(pd.DataFrame(response))

test_batch()