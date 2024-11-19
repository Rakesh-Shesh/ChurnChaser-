
import speech_recognition as sr
import pyttsx3

class VoiceRecognitionAgent:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio_data = self.recognizer.record(source, duration=5)
            print("Recognizing...")
            text = self.recognizer.recognize_google(audio_data)
            return text

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == "__main__":
    agent = VoiceRecognitionAgent()
    while True:
        try:
            text = agent.listen()
            print("You said: ", text)
            agent.speak(f"You said {text}")
        except Exception as e:
            print(str(e))
            agent.speak("Sorry, I couldn't understand. Can you please repeat?")
