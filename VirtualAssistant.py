#! python3
# virtualAssistant.py - virtual assistant

from os import system, times
import sys
from tkinter import E
from urllib import response
from pyttsx3 import engine
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyjokes
import wikipedia
import Engine

vReciever = sr.Recognizer()
vEngine = pyttsx3.init()
voices = vEngine.getProperty('voices')
vEngine.setProperty('voice', voices[1].id)
Engine.Engine.scriptLoader(Engine.Engine,"Eliza-script.txt")

def communicate(text):
    print(text)
    vEngine.say(text)
    vEngine.runAndWait()


def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = vReciever.listen(source)
            command = vReciever.recognize_google(voice)
            command = command.lower()
            if 'eliza' in command:
                command.replace('eliza', '')
                print(command)
    except Exception as e:
        pass
    return command

def runBaba():
    command = take_command()
    print("Your input: "+command)
    if 'play' in command:
        song = command.replace('play', '')
        communicate('playing'+song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I: %M %p')
        communicate('Current time is ' + time)
    elif 'joke' in command:
        communicate(pyjokes.get_joke())
    elif 'quit' in command:
        communicate(Engine.Engine.finalMessage(Engine.Engine))
        sys.exit("Exited")  
    else:
        response = Engine.Engine.run(Engine.Engine,command)
        communicate(response)

def startAss():
    communicate(Engine.Engine.initialMessage(Engine.Engine))
    while True:
        runBaba()

startAss()