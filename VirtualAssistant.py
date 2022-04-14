#! python3
# virtualAssistant.py - virtual assistant

from os import system, times
from pyttsx3 import engine
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyjokes
import wikipedia

vReciever = sr.Recognizer()
vEngine = pyttsx3.init()
voices = vEngine.getProperty('voices')
vEngine.setProperty('voice', voices[1].id)

def communicate(text):
    print(text)
    vEngine.say(text)
    vEngine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = vReciever.listen(source)
            command = vReciever.recognize_google(voice)
            command = command.lower()
            if 'baba' in command:
                command.replace('baba', '')
                print(command)
    except:
        pass
    return command

def runBaba():
    command = take_command()
    print(command)
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
        print('do you want to quit? ')
    else:
        communicate('Please repeat your query again')


while True:
    runBaba()
    print('finished iteration')
print('Exiting')
communicate('Exiting')