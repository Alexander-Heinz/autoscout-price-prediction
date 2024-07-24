# Final Project

# Dataset:
- German used cars dataset (Autoscout24)
- Data exploration notebook, missing value removal, for pipeline
- pipeline steps


Tracking with MLFlow

1. install mlflow
`pip install mlflow`

2. configure mlflow
- run `mlflow` in the console to see all commands

- run `mlflow ui --backend-store-uri sqlite:///mlflow.db` to run mlflow with a sqlite database

- put `mlflow.set_tracking_uri("sqlite:///mlflow.db")` into your code to set the tracking URI

- put `mlflow.set_experiment({your_experiment_name})` to set the experiment name

- use `with mlflow.start_run():` and `mlflow.log_param()` or `mlflow.log_metric()` to track your parameters and metrics

- to safely shut down mlflow, use these commands:


`sudo lsof -i -P -n | grep 8080`
lists active processes at port 8080

`sudo kill <id>`

kills the port by the ID which is listed in the active processes.


3. Use mage
- After opening up Docker, in the scripts directory, run `sh start.sh`


*Problem description*
For my MLOps final project, I utilized the Autoscout24 German used car dataset to develop a comprehensive machine learning pipeline. The project involved creating a predictive model to estimate car prices based on various features like make, model, year, mileage, and more.

Key steps included:

Data Preprocessing: Cleaning and preparing the data for modeling.
Model Development: Training and evaluating multiple predictive models to select the best one.
Model Deployment: Containerizing the model using Docker and deploying it on a cloud platform.
Monitoring and Maintenance: Implementing continuous monitoring to track model performance and data drift, ensuring the model remains accurate over time.
This project demonstrated my ability to manage the entire machine learning lifecycle, from data processing to deployment and ongoing model management, reflecting practical MLOps practices.



# Instructions

