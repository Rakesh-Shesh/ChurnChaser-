
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
from matplotlib import pyplot as plt

class SalesForecastingAgent:
    def __init__(self, data_file):
        self.data_file = data_file
        self.model = None
        self.data = None

    def load_data(self):
        # Load the data from a CSV file
        self.data = pd.read_csv(self.data_file)
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.data.set_index('Date', inplace=True)

    def train(self):
        # Train the ARIMA model
        self.model = ARIMA(self.data, order=(5,1,0)) # The order parameter may need to be adjusted
        self.model_fit = self.model.fit(disp=0)

    def forecast(self, steps):
        # Use the model to make a forecast
        forecast, stderr, conf_int = self.model_fit.forecast(steps=steps)
        return forecast

    def visualize(self):
        # Visualize the data and the forecast
        self.data.plot()
        plt.show()

if __name__ == "__main__":
    agent = SalesForecastingAgent('sales_data.csv')
    agent.load_data()
    agent.train()
    forecast = agent.forecast(5)  # forecast the next 5 periods
    print(f"Forecast: {forecast}")
    agent.visualize()
