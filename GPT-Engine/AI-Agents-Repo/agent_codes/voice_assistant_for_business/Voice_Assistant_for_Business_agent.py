
import speech_recognition as sr
import pyttsx3
import datetime
import os

class BusinessAssistant:
    def __init__(self, name):
        self.name = name
        self.engine = pyttsx3.init()

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('Listening...')
            audio = r.listen(source)

        try:
            print('Recognizing...')
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print(e)
            print('Say that again, please...')
            return "None"
        return query

    def run(self):
        self.speak('Hello, how can I assist you?')
        while True:
            query = self.listen().lower()
            if 'time' in query:
                self.tell_time()
            elif 'open file' in query:
                self.open_file(query)
            # add more commands here

    def tell_time(self):
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        self.speak(f"The time is {strTime}")

    def open_file(self, query):
        # This is a simple example, modify to suit your needs
        filename = query.split(' ')[-1]
        try:
            os.system(f'open {filename}')
        except Exception as e:
            self.speak('Sorry, I could not open the file.')

if __name__ == '__main__':
    assistant = BusinessAssistant('Voice Assistant for Business')
    assistant.run()
