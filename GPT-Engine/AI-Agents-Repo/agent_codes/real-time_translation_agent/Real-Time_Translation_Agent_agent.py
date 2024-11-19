
# Importing necessary libraries
from googletrans import Translator, LANGUAGES

# Defining the Translation Agent Class
class RealTimeTranslationAgent:
    def __init__(self):
        self.translator = Translator()

    def translate_text(self, text, dest_lang='en'):
        if dest_lang not in LANGUAGES.values():
            raise ValueError(f"Unsupported language code: {dest_lang}")
        
        translated = self.translator.translate(text, dest=dest_lang)
        return translated.text

    def detect_language(self, text):
        detected = self.translator.detect(text)
        return LANGUAGES[detected.lang]

# Testing the Translation Agent
if __name__ == "__main__":
    agent = RealTimeTranslationAgent()
    
    text = 'Hola, �C�mo est�s?'
    detected_lang = agent.detect_language(text)
    print(f'Detected Language: {detected_lang}')
    
    translated_text = agent.translate_text(text, 'en')
    print(f'Translated Text: {translated_text}')
