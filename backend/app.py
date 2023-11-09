import flask
from typing import List, Dict
from flask import Flask
import json
from openai import OpenAI
from flask_cors import CORS
from pathlib import Path

app = Flask(__name__)

CORS(app, resources={r"/chat": {"origins": "http://localhost:3000"}})

here = Path(__file__)

with open(here.parent / "config.json", "r") as handle:
    config = json.load(handle)
with open(here.parent / "system_message.txt") as handle:
    system_message = handle.read()


@app.route("/chat", methods=["POST"])
def chat():
    conversation_history = flask.request.json['message']
    print(conversation_history)
    modified_conversation_history = [{"role": "system", "content": system_message}] + conversation_history
    response = ask_chatgpt(messages=modified_conversation_history)
    print(response)
    conversation_history.append({"role": "assistant", "content": response})
    print(conversation_history)
    return flask.jsonify({'message': conversation_history})


def ask_chatgpt(messages: List[Dict[str, str]]) -> str:
    client = OpenAI(api_key=config["openai-api-key"])
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    app.run()

