from flask import Flask, render_template, request
import os
import openai
import win32com.client
import speech_recognition as sr
import os
import webbrowser
import openai
import numpy as np
import win32com.client
from dotenv import load_dotenv

load_dotenv()  

app = Flask(__name__)

# Initialize OpenAI API
openai.api_key = os.getenv("apikey")

# Initialize SAPI voice for speech output
Speaker = win32com.client.Dispatch("SAPI.SpVoice")

chatStr = ""

def chat(query):
    global chatStr
    chatStr += f"User: {query}\nAssistant: "
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    assistant_response = response["choices"][0]["text"]
    chatStr += f"{assistant_response}\n"
    
    return assistant_response

def ai(prompt):
    text = f"   *****   Your Prompt: {prompt} *****\n\n"
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    assistant_response = response["choices"][0]["text"]
    # say(assistant_response)
    
    text += assistant_response
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)

def say(text):
    Speaker.Speak(str(text))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_input = request.form['user_input']
        if "question" in user_input:
            ai(user_input)
        else:
            response = chat(user_input)
            ai_response = "Sunil 2.0: " + response
            return render_template('index.html', ai_response=ai_response)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
