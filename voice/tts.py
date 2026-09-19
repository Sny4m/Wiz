import random

import pyttsx3


GREETINGS = [
    "Good evening, Sanyam. WIZ is online. Your system is ready.",
    "Hey Sanyam. WIZ is up and running. Let's get to work.",
    "Welcome back. WIZ is online and listening.",
    "Good evening. Systems are ready. What are we building today?",
    "WIZ online. Everything looks ready. Let's make something happen.",
    "Hey. I'm online, your laptop is ready, and I'm listening.",
]


def _engine():
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    return engine


def speak(text):
    if not text:
        return

    try:
        engine = _engine()
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception:
        # TTS must never break the terminal UI.
        pass


def startup_greeting():
    return random.choice(GREETINGS)
