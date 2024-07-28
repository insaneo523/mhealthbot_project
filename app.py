import google.generativeai as genai
import logging
import absl.logging
from flask import Flask, request, jsonify, render_template

# Configure logging to suppress warnings and info messages
logging.getLogger('absl').setLevel(logging.ERROR)
logging.getLogger('absl.logging').setLevel(logging.ERROR)

# Directly configure API key
genai.configure(api_key='AIzaSyDyoHIMhQZ9zpcsdeZy00h69I-dx2LAzH8')

model = genai.GenerativeModel('gemini-1.5-flash')

# Function to get a response from the Gemini API
def get_gemini_response(history, user_input):
    try:
        prompt = '\n'.join(history + [f"User: {user_input}", "EmpathyBot:"])
        response = model.generate_content(prompt)
        if response:
            return response.text.strip()
        else:
            return "I'm sorry, I couldn't understand that. Can you please rephrase?"
    except Exception as err:
        return "I'm experiencing some technical issues. Please try again later."

# Flask app initialization
app = Flask(__name__)

@app.route('/')
def index():
    # Initial greeting
    initial_greeting = "Hello! I am EmpathyBot. How can I assist you today?"
    return render_template('index.html', initial_greeting=initial_greeting)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    history = request.json.get('history', [])
    chatbot_reply = get_gemini_response(history, user_input)
    return jsonify({'reply': chatbot_reply})

if __name__ == '__main__':
    app.run(debug=True)
