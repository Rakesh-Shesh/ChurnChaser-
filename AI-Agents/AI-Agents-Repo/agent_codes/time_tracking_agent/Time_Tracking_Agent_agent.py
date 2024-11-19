
import datetime

class TimeTrackingAgent:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.total_time = None

    def start_tracking(self):
        self.start_time = datetime.datetime.now()
        print(f"Time tracking started at {self.start_time}")

    def stop_tracking(self):
        self.end_time = datetime.datetime.now()
        self.total_time = self.end_time - self.start_time
        print(f"Time tracking ended at {self.end_time}")

    def display_total_time(self):
        if self.total_time is not None:
            print(f"Total time tracked: {self.total_time}")
        else:
            print("No time has been tracked yet.")

if __name__ == "__main__":
    agent = TimeTrackingAgent()
    agent.start_tracking()
    input("Press enter to stop tracking...")
    agent.stop_tracking()
    agent.display_total_time()
