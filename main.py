import os
from twilio.rest import Client
import flask
from flask import send_from_directory, request
from openai import OpenAI
from typing import List
import keys


training_data = ""#read(estilo.pdf) + read(whatsapp.pdf)
import requests
import json

def assist_journalist(prompt):
    api_url = "https://reverse.mubi.tech/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Origin': 'https://gptcall.net/',
        'Referer': 'https://gptcall.net/'
    }
    data = {
        'model': keys.ai_model,
        'messages': [{'role': "user", 'content': prompt}]
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        print(f"Error sending prompt to GPT: {response.status_code} {response.text}")
        return f"Error: {response.text}"
    else:
        return response.json()["choices"][0]["message"]["content"]

app = flask.Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/favicon.png')

@app.route('/')
@app.route('/home')
def home():
    return "Hello World"

clients = {}

ACCOUNT_SID = keys.twilio_sid
AUTH_TOKEN = keys.twilio_token

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def mensaje(number, text):
    message = client.messages.create(
     from_=keys.twilio_number,
     body=text,
     to=number
    )
    print(message.sid)

def mensaje_nuevo(tlf, message, name):
    telephone = "whatsapp:+" + tlf
    if message == "{clients}":
        mensaje(telephone, clients)
        if training_data == "":
            mensaje(telephone, "Los datos de entrenamiento no están disponibles. Sorry!")
        else:
            mensaje(telephone, training_data) 
    else:
        send = assist_journalist(keys.prompt + "Tu nombre es " + keys.bot_name + str("El cliente te ha dicho: " + message) + "La persona que te contacta se llama" + name)
        mensaje(telephone, send)
    return send

@app.route('/', methods=['GET', 'POST'])
def whatsapp():
    message = request.form['Body']
    name = request.form['ProfileName']
    senderId = request.form['From'].split('+')[1]
    response = mensaje_nuevo(senderId, message, name)
    os.system("cls")
    print("###############################")
    print()
    print(f'Message --> {message}')
    print(f'Tlf number --> {senderId}')
    print(f'Name --> {name}')
    print(f'AI response --> {response}')
    print()
    print("###############################")
    return "lol"

if __name__ == "__main__":
    app.run(port=keys.ngrok_port, debug=True)
