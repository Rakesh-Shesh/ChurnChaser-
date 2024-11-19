
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

class ForecastingAgent:

    def __init__(self, data):
        self.data = pd.read_csv(data)
        self.model = LinearRegression()

    def preprocess(self):
        self.data = self.data.dropna()
        X = self.data['Supply'].values.reshape(-1,1)
        y = self.data['Demand'].values.reshape(-1,1)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    def train(self):
        self.model.fit(self.X_train, self.y_train)

    def predict(self, supply):
        return self.model.predict([[supply]])

    def evaluate(self):
        y_pred = self.model.predict(self.X_test)
        print('Mean Absolute Error:', metrics.mean_absolute_error(self.y_test, y_pred))
        print('Mean Squared Error:', metrics.mean_squared_error(self.y_test, y_pred))
        print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(self.y_test, y_pred)))

if __name__ == "__main__":
    agent = ForecastingAgent('supply_demand_data.csv')
    agent.preprocess()
    agent.train()
    agent.evaluate()
    print(agent.predict(100))
