
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Name the ChatBot 'Lead Generation Chatbot'
chatbot = ChatBot('Lead Generation Chatbot')

# Use the ChatterBotCorpusTrainer
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot using English corpus data
trainer.train(
    "chatterbot.corpus.english.greetings",
    "chatterbot.corpus.english.conversations"
)

# Get a response from the chatbot
response = chatbot.get_response("Hello, how can I help you?")
print(response)
