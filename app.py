from flask import Flask, request, jsonify, render_template
import random
import openai
import os

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Training data and fallback responses
training_data = {
    "Question": {
        "inputs": ["how are you doing", "Why are you doing this?", "are you a person?", "What's up", "do you want to go to NYC?", "hey what's up"],
        "responses": ["dude don't ask me", "yea yea", "idk bro idk"]
    },
    "Love": {
        "inputs": ["I love you", "you're so cute", "you look so beautiful", "how are you this beautiful?"],
        "responses": ["yea yea", "bleh", "debatable", "ehh", "yea ik", "booo"]
    },
    "Sexual": {
        "inputs": ["i wanna eat you", "you're so hot", "you're sexy babe", "i wanna kiss you"],
        "responses": ["Ewwwwwwww", "you're weird", "booo"]
    }
}

fallback_responses = [
    "you're a watermelon squash", 
    "wanna help me murder somebody?", 
    "ur boring", 
    "i'm gonna sleep", 
    "Kay Kay", 
    "yea idc", 
    "whatever", 
    "Sleep?",
    "You raccoon",
    "ur a nincompoop",
    "whatever broski"
]

# GPT classification
def gpt_classify(user_input):
    messages = [
        {"role": "system", "content": "You are a classifier that categorizes user input into one of these categories: Question, Love, Sexual."},
        {"role": "user", "content": f"Classify this input: '{user_input}' into one of the categories: Question, Love, Sexual. Respond with only the category name."}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.0
    )
    category = response['choices'][0]['message']['content'].strip()
    return category if category in training_data.keys() else None

# Get response logic
def get_response(user_input):
    if random.random() < 0.5:  # 50% chance for fallback
        return random.choice(fallback_responses)

    category = gpt_classify(user_input)
    if category:
        return random.choice(training_data[category]["responses"])
    else:
        return random.choice(fallback_responses)

# Serve the UI
@app.route('/')
def home():
    return render_template('index.html')

# Chat endpoint for backend
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')
    if not user_input:
        return jsonify({"error": "Message is required!"}), 400
    response = get_response(user_input)
    return jsonify({"response": response})
