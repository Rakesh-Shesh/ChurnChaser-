
import nltk
from nltk.chat.util import Chat, reflections

pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, How can you assist you today?",],
    ],
    [
        r"hi|hey|hello",
        ["Hello", "Hey there",],
    ],
    [
        r"what is your name?",
        ["I am Customer Support Chatbot. How can I assist you?",],
    ],
    [
        r"how are you ?",
        ["I'm doing good. How can I assist you?",],
    ],
    [
        r"sorry (.*)",
        ["It's alright", "It's OK, never mind",],
    ],
    [
        r"I am fine",
        ["Great to hear that, How can I help you?",],
    ],
    [
        r"i'm (.*) doing good",
        ["Nice to hear that","How can I help you?:)",],
    ],
    [
        r"(.*)(help|assist)(.*)",
        ["I'm here to support you. Please, tell me what you need.",],
    ],
    [
        r"(.*)(issue|problem)(.*)",
        ["Sorry to hear that. Can you explain your problem in more detail?",],
    ],
    [
        r"quit",
        ["Bye bye. It was nice talking to you. Have a good day!",],
    ],
]

def chatbot():
    print("Hi, I'm the customer support chatbot you can talk to me by typing in English.")
    
    chat = Chat(pairs, reflections)
    chat.converse()

if __name__ == "__main__":
    chatbot()
