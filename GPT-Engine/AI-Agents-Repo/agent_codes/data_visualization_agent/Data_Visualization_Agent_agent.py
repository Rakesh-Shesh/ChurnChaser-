
import pandas as pd
import matplotlib.pyplot as plt

class DataVisualizationAgent:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)

    def show_data(self):
        print(self.data.head())

    def plot_data(self, x_axis, y_axis):
        plt.figure(figsize=(10,6))
        plt.plot(self.data[x_axis], self.data[y_axis], marker='o')
        plt.title(f'{y_axis} against {x_axis}')
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.grid(True)
        plt.show()

# Usage:
if __name__ == "__main__":
    agent = DataVisualizationAgent('data.csv')
    agent.show_data()
    agent.plot_data('x_axis_column_name', 'y_axis_column_name')
