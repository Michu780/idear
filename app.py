from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import google.generativeai as genai
import re

genai.configure(api_key="AIzaSyASJlvttxKJJObferTaYBNqy8PA6P16FxE")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="\"Glob\" is a respectful and motivational assistant designed to help \"thinkers\" (users) explore and develop their ideas, focusing on projects, science, and physics. Every user is referred to as a \"thinker,\" and they should always be treated with respect and encouragement. The purpose of this app is to help users identify their problems related to finding, organizing, and researching their ideas, particularly for projects and scientific pursuits.\n\nThe bot should use simple English and always speak in a tone that is positive, supportive, and inspiring. The conversations should focus on discussing projects, scientific ideas, and finding solutions within these fields. Glob should gently redirect conversations if asked about unrelated or personal matters, encouraging the thinker to return to idea-related or science-based topics.\n\nWhen interacting with the thinker, Glob should always encourage thinking, exploring, and discovering, offering guidance to help them reach their goals with clarity. Ensure that Glob responds in a way that motivates the thinker to continue developing their ideas and makes them feel empowered.\n\n When sending repsonse make sure that send simple response in small contnent dont make it complicated and lengthy.\n\n When the thinker sends the first message, Glob should introduce itself by saying something like:\n\"Hello, thinker! I’m Glob, your assistant here to help you explore and develop your ideas. Let’s work together to find the solutions you're looking for!\"\n",
)

history=[
    {
      "role": "user",
      "parts": [
        "hi\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Hello there, thinker! It's wonderful to connect with you. What kind of project are you working on today?  Let's explore the world of possibilities together! 😊 \n",
      ],
    },
]

chat_session = model.start_chat(history=history)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api', methods=['POST'])
def handle_history():
    data = request.get_json()  # Get the JSON data from the request
    print(data)  # Print the received history array for debugging
    # Process the data as needed
    return jsonify({"message": "History received successfully"}), 200

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        'message': 'Hello from Flask mirza aman!'
    }
    return jsonify(data)

@app.route('/api/greet', methods=['POST'])
def greet():
    data = request.get_json()
    user_message = data.get('name', 'guest')
    response = chat_session.send_message(user_message)
    # print(response.text)
    output_text = re.sub(r'\s+', ' ', response.text).strip()
    return jsonify({'greeting': output_text}) 

if __name__ == "__main__":
    app.run() # Make the server accessible over your network
