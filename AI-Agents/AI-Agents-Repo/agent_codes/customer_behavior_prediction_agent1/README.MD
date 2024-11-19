# Customer Behavior Prediction Agent

## Overview

The **Customer Behavior Prediction Agent** is a sophisticated system designed to predict customer behaviors (e.g., purchase likelihood, churn potential) using machine learning models. The agent is built to handle data processing, real-time predictions, model evaluation, database integration, and email notifications. It also includes a model interpretation feature using SHAP to explain predictions, making it more transparent and understandable.

## Features

- **Model Training & Evaluation**: The agent trains a Random Forest Classifier model on customer behavior data and evaluates its performance.
- **Database Integration**: Stores the model's performance metrics (accuracy, classification report) into a PostgreSQL database for future tracking and analysis.
- **Email Notifications**: Sends notifications via email to alert the marketing team about high-potential customers or other important behavior predictions.
- **Model Saving & Retraining**: Saves the trained model using `joblib` and supports periodic retraining on new data.
- **Model Explanation with SHAP**: Uses SHAP (SHapley Additive exPlanations) for interpreting the model’s predictions and visualizing feature importances.
- **Real-Time Predictions**: Provides functionality to make predictions for new customers or customer data via the `CustomerBehaviorPredictionAgent` class.

## Prerequisites

- Python 3.x
- Dependencies:
  - `pandas`
  - `numpy`
  - `scikit-learn`
  - `shap`
  - `sqlalchemy`
  - `joblib`
  - `smtplib`
  - PostgreSQL (or another database of your choice)

To install the necessary libraries, use the following command:

```bash
pip install pandas numpy scikit-learn shap sqlalchemy smtplib joblib
