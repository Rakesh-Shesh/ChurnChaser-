
import pandas as pd
import numpy as np

class DataCleaningAgent:

    def __init__(self, dataframe):
        self.dataframe = dataframe

    # Method to handle missing values
    def handle_missing_values(self):
        # fill numerical missing values with mean
        for column in self.dataframe.select_dtypes(include=[np.number]).columns:
            self.dataframe[column].fillna(self.dataframe[column].mean(), inplace=True)
        # fill non-numerical missing values with mode
        for column in self.dataframe.select_dtypes(exclude=[np.number]).columns:
            self.dataframe[column].fillna(self.dataframe[column].mode()[0], inplace=True)
        return self.dataframe

    # Method to remove duplicates
    def remove_duplicates(self):
        self.dataframe.drop_duplicates(inplace=True)
        return self.dataframe

    # Method to convert data types to a specified type
    def convert_data_type(self, column, dtype):
        self.dataframe[column] = self.dataframe[column].astype(dtype)
        return self.dataframe

# Testing the DataCleaningAgent
df = pd.read_csv('Test.csv') # replace with your csv file path

agent = DataCleaningAgent(df)

# Handle missing values
df = agent.handle_missing_values()

# Remove duplicates
df = agent.remove_duplicates()

# Convert data type of a column
df = agent.convert_data_type('ColumnName', 'int') # replace 'ColumnName' with your column name
