import pickle
from data_cleaner import DataCleaner
from flask import Flask, request, jsonify
import pandas as pd

with open('mdl_pipeline.bin', 'rb') as f_in:
    (model) = pickle.load(f_in)


def prepare_features(car_data):
    cleaner = DataCleaner(car_data)
    cleaner.clean_data()
    features = cleaner.get_features()
    return features


def predict(features):
    preds = model.predict(features)
    return float(preds[0])


app = Flask('autoscout-price-prediction')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    print("raw request:", request)

    car_data = request.get_json()
    print("request json:", car_data)

    car_data = pd.DataFrame([car_data])

    print("request df:", car_data)

    features = prepare_features(car_data)
    pred = predict(features)

    print(pred)

    result = {
        'price': pred
    }
    print(result)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)