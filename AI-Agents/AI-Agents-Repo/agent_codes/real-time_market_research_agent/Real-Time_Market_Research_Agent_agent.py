
import requests
from bs4 import BeautifulSoup
import time

class MarketResearchAgent:
    def __init__(self, url):
        self.url = url

    def get_web_data(self):
        try:
            response = requests.get(self.url)
            return response.text
        except Exception as e:
            print("An error occurred while trying to fetch data from the web: ", str(e))
            return None

    def parse_data(self, web_data):
        try:
            soup = BeautifulSoup(web_data, 'html.parser')
            market_data = soup.find_all('div', {'class':'market-data'})
            return market_data
        except Exception as e:
            print("An error occurred while trying to parse the web data: ", str(e))
            return None

    def run_agent(self):
        while True:
            web_data = self.get_web_data()
            if web_data:
                market_data = self.parse_data(web_data)
                print("Market data: ", market_data)
            time.sleep(60)  # wait for 60 seconds before fetching the data again

if __name__ == "__main__":
    url = "https://www.example.com"  # enter your URL here
    agent = MarketResearchAgent(url)
    agent.run_agent()
