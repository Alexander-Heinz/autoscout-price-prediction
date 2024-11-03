import requests
from flask import Flask, request, jsonify

car_data = {
"brand" : "Opel",
"model" : "Corsa D",
"transmission_type": "Manual",
"power_ps" : 60,
"year" : 2010,
"mileage_in_km" : 165000
}
print(car_data)
url = 'http://localhost:9696/predict'

response = requests.post(url, json=car_data)

print(response.json())

