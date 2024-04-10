import os
import time

def easeInSine(t):
    import math
    return -math.cos(t * math.pi / 2) + 1

def install(libraries):
    for library in libraries:
        os.system("pip uninstall -y " + library)
    for library in libraries:
        os.system("pip install " + library)
    os.system("cls")

def good_say(text):
    say = ""
    wait = 0
    number = 0
    for char in text:
        number += 1
        say = say + char
        os.system("cls")
        print(say + "_")
        wait = easeInSine(number / len(text))
        wait = wait / 5
        time.sleep(wait)
    os.system("cls")
    print(say)


install(["flask", "twilio", "typing", "colorama", "requests"])
good_say("Done! Run the main.py file to start the bot!")