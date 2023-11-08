import flask
from typing import List, Dict
from flask import Flask
import json
from openai import OpenAI
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/chat": {"origins": "http://localhost:3000"}})

with open("config.json", "r") as handle:
    config = json.load(handle)

conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]


@app.route("/chat", methods=["POST"])
def chat():
    user_message = flask.request.json['message']
    print(user_message)
    conversation_history.append({"role": "user", "content": user_message})
    print(conversation_history)
    response = ask_chatgpt(messages=conversation_history)
    print(response)
    conversation_history.append({"role": "assistant", "content": response})
    print(conversation_history)
    return flask.jsonify({'response': response})


def ask_chatgpt(messages: List[Dict[str, str]]) -> str:
    client = OpenAI(api_key=config["openai-api-key"])
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    app.run()

