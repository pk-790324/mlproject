import os
import sys
from dataclasses import dataclass
from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object,evaluate_models



@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()
    
    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info('split training and test input data')
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1], #select all columns except the last one.
                train_array[:,-1], #select the last column only.
                test_array[:,:-1],
                test_array[:,-1]

            )
            models={
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "K-Nearest Regressor":KNeighborsRegressor(),
                "XGBoost Regressor":XGBRegressor(),
                "CatBoosting Regressor":CatBoostRegressor(verbose=False),
                "AdaBoost Regressor":AdaBoostRegressor(),
            }
            params={
                "Decision Tree":{
                    'criterion':['squared_error','friedman_mse','absolute_error','poisson'],
                    'splitter':['best','random'],
                    'max_features':['sqrt','log2']
                },
                "Random Forest":{
                    'criterion':['squared_error','friedman_mse','absolute_error','poisson'],
                    'max_features':['sqrt','log2'],
                    'n_estimators':[8,16,32,64],
                },
                "Gradient Boosting":{
                    "learning_rate":[0.1,0.01,0.05,0.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    'n_estimators':[8,16,32,64],
                },
                "Linear Regression":{},
                "K-Nearest Regressor":{
                    'n_neighbors':[5,7,9,11],
                    'algorithm':['ball_tree','kd_tree','brute']
                },
                "XGBoost Regressor":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators':[8,16,32,64,128]
                },
                "CatBoosting Regressor":{
                    'depth':[6,8,10],
                    'learning_rate':[0.1,0.01,0.05],
                    'iterations':[30,50,100]   
                },
                "AdaBoost Regressor":{
                    "learning_rate":[0.1,0.01,0.5,0.001],
                    'n_estimators':[8,16,32,64,128]
                }
            }
            model_report:dict=evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models,params=params)
            #to get best model score from dict
            best_model_score=max(sorted(model_report.values()))
            #to get best model name form dict
            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model=models[best_model_name]

            if best_model_score<0.6:
                raise CustomException("No best model found")
            logging.info(f'Best model found on both training and testing datasets:{best_model}')
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model



            )
            predicated=best_model.predict(X_test)
            r2_square=r2_score(y_test,predicated)
            return r2_square
        except Exception as e:
            raise CustomException(e,sys)
    

