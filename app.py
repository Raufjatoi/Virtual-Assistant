import streamlit as st
import speech_recognition as sr
import pyttsx3
from groq import Groq

bot = Groq(api_key="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") # i hard coded 

engine = pyttsx3.init()

def gen(prompt, system_prompt=None):
    messages = []
    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })
    messages.append({
        "role": "user",
        "content": prompt
    })
    
    response = bot.chat.completions.create(
        messages=messages,
        model="llama-3.1-8b-instant"
    )
    return response.choices[0].message.content

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        st.write("Recognizing...")
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

st.title("Virtual Assistant based on System prompt")
st.write("ask me")

if st.button("voice input"):
    user_input = recognize_speech_from_mic()
    st.write(f" u said {user_input}")
else:
    user_input = st.text_input("user prompt: ")

system_prompt = st.text_input("system Prompt (what you want it to be?):", "you are an AGI")

if user_input:
    response = gen(user_input, system_prompt)
    st.write("llama-3.1-8b-instant: ")
    st.write(response)
    
    if st.button("speak Response"):
        speak(response)