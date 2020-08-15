import pyaudio
import speech_recognition as sr
import pyttsx3 as p
import voictest as vt
import os
import subprocess
import datetime
import wikipedia
import webbrowser
import ecapture
import wolframalpha

chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'

# webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open("http://google.com")

engine = p.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1])


def speak(text):
    engine.say(text)
    engine.runAndWait()


def wish():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Hello Midun,  Good Morning")
    elif 12 <= hour < 18:
        speak("Hello Midun,  Good Afternoon")
    else:
        speak("Hello Midun,  Good Evening")


def ask():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        text = r.listen(source)
        try:
            said_text = r.recognize_google(text)
        except sr.UnknownValueError:
            speak("Pardon, can you say again")
        except sr.RequestError as e:
            speak("Request Error, check internet connection")
        return said_text


def mainfun(reqst):
    if 'wikipedia' in reqst or "search" in reqst or 'wiki' in reqst:
        # am.speak('Searching Wikipedia...')
        statement = reqst.replace("wikipedia", "")
        statement = reqst.replace("search", "")
        statement = reqst.replace("wiki", "")
        results = wikipedia.summary(statement, sentences=3)
        print(results)
        speak("According to Wikipedia")
        speak(results)

    if 'open youtube' in reqst:

        webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open("https://www.youtube.com")


    elif 'play' in reqst or 'in youtube' in reqst:
        statement = reqst.replace("in youtube", "")
        statement = reqst.replace("play", "")
        webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open(
            "https://www.youtube.com/results?search_query=" + statement)

    elif 'open google' in reqst:
        webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open("https://www.google.com")
        speak("Google chrome is open now")


    elif 'open gmail' in reqst:
        webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open("gmail.com")
        speak("Google Mail open now")

    elif 'time' in reqst:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"the time is {strTime}")


    elif "open stackoverflow" in reqst:
        webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open(
            "https://stackoverflow.com/login")
        speak("Here is stackoverflow")


    elif "take a photo" in reqst:
        ecapture.capture(0, "Anna's camera", "img.jpg")


    elif "log off" in reqst or "sign out" in reqst:
        speak("Ok , your pc will log off in 10 sec make sure you exit from all applications")
        subprocess.call(["shutdown", "/l"])
    elif 'who' in reqst or "what " in reqst or "why" in reqst:
        statement = reqst
        if 'what' in reqst:
            statement = reqst.replace("what", "")
        elif "why" in reqst:
            statement = reqst.replace("why", "")
        elif "who" in reqst:
            statement = reqst.replace("who", "")
        elif 'is' in reqst:
            statement = reqst.replace("is", "")
        elif "are" in reqst:
            statement = reqst.replace("are", "")
        app_id = "E6P6R2-U4Q63L5L2A"
        client = wolframalpha.Client(app_id)
        res = client.query(statement)
        answer = next(res.results).text
        speak(answer)

    else:
        try:
            app_id = "E6P6R2-U4Q63L5L2A"
            client = wolframalpha.Client(app_id)
            res = client.query(reqst)
            answer = next(res.results).text
            speak(answer)
        except :
            speak("Unknown command, please say correctly")


wish()
speak("How may i help you")
while True:
    recognised_Text = ask().lower()
    print(recognised_Text)
    if "goodbye" in recognised_Text or "ok bye" in recognised_Text:
        recognised_Ans = vt.chat(recognised_Text)
        speak(recognised_Ans)
        break
    elif recognised_Text in vt.questions:
        recognised_Ans = vt.chat(recognised_Text)
        speak(recognised_Ans)
    else:
        mainfun(recognised_Text)
