
import tweepy

class SocialMediaAnalyticsAgent:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api = self.authenticate()

    def authenticate(self):
        auth = tweepy.OAuthHandler(self.api_key, self.api_secret)
        api = tweepy.API(auth)
        return api

    def get_user_stats(self, username):
        user = self.api.get_user(username)

        return {
            "followers_count": user.followers_count,
            "friends_count": user.friends_count,
            "statuses_count": user.statuses_count
        }

if __name__ == "__main__":
    # Initialize the agent
    agent = SocialMediaAnalyticsAgent("your_api_key", "your_api_secret")

    # Get and print out user stats
    user_stats = agent.get_user_stats("example_username")
    for key, value in user_stats.items():
        print(f"{key}: {value}")
