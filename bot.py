from flask import Flask, request, jsonify, send_from_directory
import os
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

TOGETHER_AI_API_KEY = os.getenv("TOGETHER_AI_API_KEY")

# Serve the HTML file at the root URL
@app.route("/")
def index():
    return send_from_directory(".", "chatBotWebpage.html")

def ask_gpt(question: str) -> str:
    url = "https://api.together.xyz/v1/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_AI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        "prompt": f"Question: {question}\nAnswer:",
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("text", "").strip()
    else:
        return f"Error: {response.status_code}, {response.text}"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("question", "")
    
    if not user_message:
        return jsonify({"response": "Please provide a valid question."})

    bot_response = ask_gpt(user_message)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
