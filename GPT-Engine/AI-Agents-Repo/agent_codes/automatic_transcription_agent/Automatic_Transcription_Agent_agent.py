
# Required Libraries
import speech_recognition as sr

class AutomaticTranscriptionAgent:
    def __init__(self, language="en-US"):
        self.recognizer = sr.Recognizer()
        self.language = language

    def transcribe(self, audio_file):
        # Open the file
        with sr.AudioFile(audio_file) as source:
            # Read the audio file
            audio_data = self.recognizer.record(source)
            # Transcribe the audio to text
            text = self.recognizer.recognize_google(audio_data, language=self.language)
            return text

    def transcribe_from_microphone(self):
        # Get audio from the microphone
        with sr.Microphone() as source:
            print("Listening...")
            audio_data = self.recognizer.record(source)
            print("Transcribing...")
            text = self.recognizer.recognize_google(audio_data, language=self.language)
            return text

if __name__ == "__main__":
    agent = AutomaticTranscriptionAgent()
    
    # Transcribe an audio file
    transcription = agent.transcribe("audio_file.wav")
    print("Transcription: ", transcription)

    # Transcribe from microphone
    transcription = agent.transcribe_from_microphone()
    print("Transcription: ", transcription)


