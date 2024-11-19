
import urllib.request
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

class SEOOptimizationAgent:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.text = None
        self.tokens = None
        self.frequencies = None

    def fetch_website(self):
        try:
            html = urllib.request.urlopen(self.url)
            self.soup = BeautifulSoup(html, features="html.parser")
            for script in self.soup(["script", "style"]):
                script.extract()
            self.text = self.soup.get_text()
        except Exception as e:
            print(f"Error fetching website: {e}")
            return

    def analyze_content(self):
        try:
            stop_words = set(stopwords.words('english'))
            word_tokens = word_tokenize(self.text)
            filtered_text = [w for w in word_tokens if not w in stop_words]
            self.tokens = filtered_text
            self.frequencies = Counter(self.tokens)
        except Exception as e:
            print(f"Error analyzing content: {e}")
            return
    
    def suggest_keywords(self, num_keywords=10):
        try:
            most_common = self.frequencies.most_common(num_keywords)
            for word, freq in most_common:
                print(f"Keyword: {word}, Frequency: {freq}")
        except Exception as e:
            print(f"Error suggesting keywords: {e}")
            return
        
if __name__ == "__main__":
    agent = SEOOptimizationAgent("http://www.example.com")
    agent.fetch_website()
    agent.analyze_content()
    agent.suggest_keywords()
