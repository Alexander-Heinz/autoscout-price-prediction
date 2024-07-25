## Deploying a model as a web-service

Used the instructions from the course:

* Creating a virtual environment with Pipenv
* Creating a script for predictiong 
* Putting the script into a Flask app
* Packaging the app to Docker


```bash
docker build -t autoscout-price-prediction:v1 .
```

```bash
docker run -it --rm -p 9696:9696  autoscout-price-prediction:v1
```


run `python test.py` to test the batch prediction using the web service
