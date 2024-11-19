
from textblob import TextBlob

class SentimentAnalysisAgent:
    def __init__(self):
        pass

    def analyze(self, text):
        testimonial = TextBlob(text)
        polarity = testimonial.sentiment.polarity
        subjectivity = testimonial.sentiment.subjectivity

        if polarity > 0:
            sentiment = 'Positive'
        elif polarity < 0:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        
        return sentiment, polarity, subjectivity

if __name__ == "__main__":
    agent = SentimentAnalysisAgent()
    text = "I love this library. It's extremely useful and easy to use."
    sentiment, polarity, subjectivity = agent.analyze(text)
    print(f'Sentiment: {sentiment}, Polarity: {polarity}, Subjectivity: {subjectivity}')
