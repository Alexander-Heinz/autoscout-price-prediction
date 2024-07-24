# Final Project

*Problem description*
For my MLOps final project, I utilized the Autoscout24 German used car dataset to develop a comprehensive machine learning pipeline. The project involved creating a predictive model to estimate car prices based on various features like make, model, year, mileage, and more.

Key steps included:

- Data Preprocessing: Cleaning and preparing the data for modeling
    - see `jupyter_notebooks` folder for my first inspection of the dataset
- Model Development: Training and evaluating a xgboost model using mlflow as a monitoring tool and mage as orchestration framework
    - saving the best model using pickle and storing the best parameters as json and inside mlflow
    - validation on a batch dataset from a different source

- Model Deployment: Containerizing the model using Docker and deploying it as a web service.

*To Do's:*
- graphical user interface to allow users to estimate the price of their used cars
- price range estimation instead of point estimate
- cloud deployment
- data drift checks using new data
- new data scraping scripts for continuous scraping on the autoscout24 web page



# Instructions

#### Training, model monitoring & saving a model


- To get started, run `scripts/run.sh`  (go to the `scripts` directory and run `sh run.sh` in your terminal)

- This will run the `docker-compose` for mage, mlflow and the database, as in the third module of the course

- open mage (using [localhost:](http://localhost:6789/overview)) and go to pipelines -> data_prep

- the code is set to 2 runs to find the best parameters. Change `n_evals` in the modeling step to a higher integer for a possibly better model. 

- if a `best_params.json` file is inside the `models` directory, the code will use these parameters and not tune the model.

- run the pipeline to test it and see the performance on the validation batch dataset from a different source


#### web service

- Locate to the `webservice` directory

- follow the instructions in the `README.md`