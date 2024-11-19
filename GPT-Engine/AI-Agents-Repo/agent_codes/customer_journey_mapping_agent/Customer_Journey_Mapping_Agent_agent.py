
import pandas as pd

class CustomerJourneyMappingAgent:

    def __init__(self, data_source):
        self.data_source = data_source
        self.data = pd.read_csv(self.data_source)
        self.journey_map = {}

    def preprocess_data(self):
        self.data = self.data.sort_values(['customer_id', 'timestamp'])
        self.data['stage'] = self.data['stage'].fillna('Unknown') 
        
    def map_customer_journey(self):
        for index, row in self.data.iterrows():
            customer_id = row['customer_id']
            stage = row['stage']
            if customer_id in self.journey_map:
                self.journey_map[customer_id].append(stage)
            else:
                self.journey_map[customer_id] = [stage]
                
    def get_customer_journey(self, customer_id):
        if customer_id in self.journey_map:
            return self.journey_map[customer_id]
        else:
            return None

if __name__ == "__main__":
    agent = CustomerJourneyMappingAgent('customer_data.csv')
    agent.preprocess_data()
    agent.map_customer_journey()

    # Get journey for a specific customer
    print(agent.get_customer_journey('customer_id_1'))
