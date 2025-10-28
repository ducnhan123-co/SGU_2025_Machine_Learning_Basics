"""
Configuration file for Titanic ML Project
Centralized configuration for easy management
"""

import os

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
PROCESS_DIR = os.path.join(PROJECT_ROOT, "process")
EXPS_DIR = os.path.join(PROCESS_DIR, "exps")

# Model parameters
MODELS = {
    'logistic_regression': {
        'scaler': True,
        'param_grid': {
            'logreg__C': [0.01, 0.1, 1, 10, 100],
            'logreg__penalty': ['l1', 'l2'],
            'logreg__solver': ['liblinear']
        }
    },
    'random_forest': {
        'scaler': True,
        'param_grid': {
            'rf__n_estimators': [50, 100, 200],
            'rf__max_depth': [3, 5, 7, None],
            'rf__min_samples_split': [2, 5, 10],
            'rf__min_samples_leaf': [1, 2, 4],
            'rf__max_features': ['sqrt', 'log2', None]
        }
    },
    'xgboost': {
        'scaler': True,
        'param_grid': {
            'xgb__n_estimators': [50, 100, 200],
            'xgb__max_depth': [3, 5, 7],
            'xgb__learning_rate': [0.01, 0.1, 0.2],
            'xgb__subsample': [0.8, 0.9, 1.0],
            'xgb__colsample_bytree': [0.8, 0.9, 1.0],
            'xgb__reg_alpha': [0, 0.1, 1],
            'xgb__reg_lambda': [1, 10, 100]
        }
    }
}

# Cross-validation
CV_CONFIG = {
    'n_splits': 5,
    'shuffle': True,
    'random_state': 42
}

# Random seed
RANDOM_SEED = 42

# Feature engineering
FEATURE_CONFIG = {
    'age_bins': [-1, 12, 22, 34, 46, 64, 100],
    'age_labels': ['Babi', 'Teen', 'Young', 'Adult', 'Mid_Age', 'Old'],
    'fare_bins': [-1, 40, 80, 200, 1000],
    'fare_labels': ['So_Cheap', 'Cheap', 'Medium', 'Expensive'],
    'knn_neighbors': 5,
    'top_titles': 5
}

# Data files
DATA_FILES = {
    'train': 'train.csv',
    'test': 'test.csv',
    'submission_template': 'gender_submission.csv'
}
