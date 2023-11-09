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

costs = []

def estimate_conversation_cost(conversation_history: List[Dict[str, str]]) -> float:
    def _estimate_message_cost(message_text: str, role: str) -> float:
        if role not in ("assistant", "user", "system"):
            print("Role not supported")
            return 0
        cost = input_cost if role in ("system", "user") else output_cost
        return len(message_text.split(" ")) * cost

    input_cost = 0.03 * 4.91
    output_cost = 0.06 * 4.91
    total_cost = 0
    for message in conversation_history:
        total_cost += _estimate_message_cost(message_text=message["content"], role=message["role"])
    return total_cost


@app.route("/chat", methods=["POST"])
def chat():
    conversation_history = flask.request.json['message']
    print(conversation_history)
    modified_conversation_history = [{"role": "system", "content": system_message}] + conversation_history
    response = ask_chatgpt(messages=modified_conversation_history)
    print(response)
    conversation_history.append({"role": "assistant", "content": response})
    print(conversation_history)
    costs.append(estimate_conversation_cost(conversation_history=conversation_history))
    print(sum(costs))
    return flask.jsonify({'message': conversation_history})


def ask_chatgpt(messages: List[Dict[str, str]]) -> str:
    client = OpenAI(api_key=config["openai-api-key"])
    chat_completion = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0
    )
    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    app.run()

