if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import mlflow
from hyperopt import fmin, tpe, hp, Trials, STATUS_OK
from hyperopt.pyll import scope
from pathlib import Path
import json
import pickle

@custom
def transform_custom(data, *args, **kwargs):
    X = data.drop('price_in_euro', axis=1)
    y = data['price_in_euro']

    # Define columns
    categorical_cols = ['brand', 'model', 'transmission_type']
    numerical_cols = ['year', 'power_ps', 'mileage_in_km']

    # Create a column transformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ])

    
    # Define the MLflow experiment
    experiment_name = "autoscout_tuning"
    tags = {'version': 'v0.2', 'type': 'demo'}
    description = "using hyperopt to hyperoptimize hyperparameters"

    # Set the tracking URI to the SQLite database
    # mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_tracking_uri("http://host.docker.internal:8080")

    # Create an experiment if it doesn't exist
    if not mlflow.get_experiment_by_name(experiment_name):
        mlflow.create_experiment(name=experiment_name,
                                tags=tags,
                                artifact_location=Path.cwd().joinpath('mlruns').as_uri())

    # Load best parameters if they exist
    best_params_path = "./models/best_params.json"
    try:
        with open(best_params_path, "r") as file:
            best_params = json.load(file)
        optimize_params = False
    except FileNotFoundError:
        best_params = None
        optimize_params = True

    # Define objective function for hyperparameter optimization
    def objective(params):
        with mlflow.start_run(run_name='Hyperparameter Optimization', description=description) as run:
            mlflow.set_tag("model", "XGBRegressor")
            mlflow.log_params(params)

            # Create a pipeline
            model_pipeline = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('model', XGBRegressor(**params))
            ])
            
            # Split the data
            from sklearn.model_selection import train_test_split
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            model_pipeline.fit(X_train, y_train)
            y_pred = model_pipeline.predict(X_test)

            # Evaluate the model
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)

            # Log metrics
            mlflow.log_metric("mse", mse)
            mlflow.log_metric("rmse", rmse)
        return {'loss': rmse, 'status': STATUS_OK}

    # Hyperparameter optimization
    if optimize_params:
        n_evals = 2 # change to 20 to in production
        print("optimizing parameters...", n_evals, " runs")
        search_space = {
            'max_depth': scope.int(hp.quniform('max_depth', 4, 100, 1)),
            'learning_rate': hp.loguniform('learning_rate', -3, 0),
            'reg_alpha': hp.loguniform('reg_alpha', -5, -1),
            'reg_lambda': hp.loguniform('reg_lambda', -6, -1),
            'min_child_weight': hp.loguniform('min_child_weight', -1, 3)
        }

        try:
            best_result = fmin(
                fn=objective,
                space=search_space,
                algo=tpe.suggest,
                max_evals=n_evals,
                trials=Trials()
            )
            best_params = best_result

            best_params["max_depth"] = int(best_params["max_depth"]) # debug faulty double storage
            # Save best parameters
            with open(best_params_path, "w") as file:
                json.dump(best_params, file)
        except Exception as e:
            print(e)
    else:
        print("Using previously found best parameters.")

    # Train final model with best parameters
    with mlflow.start_run(run_name='Final Model', description=description) as run:
        mlflow.set_tag("model", "XGBRegressor")
        mlflow.log_params(best_params)

        # Create a pipeline
        final_model_pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', XGBRegressor(**best_params))
        ])
        
        # Split the data
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        final_model_pipeline.fit(X_train, y_train)


        y_pred = final_model_pipeline.predict(X_test)

        with open('./models/mdl_pipeline.bin', 'wb') as f_out:
            pickle.dump(final_model_pipeline, f_out)

        # Evaluate the model
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)

        # Log metrics
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("rmse", rmse)


    return final_model_pipeline


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
