
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
