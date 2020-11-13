import psutil
import time
import sys
from pynput import keyboard

def processRunning(processName):
    for process in psutil.process_iter():
        try:
            if processName.lower() in process.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


kb = keyboard.Controller()
def pressKey(key, delay=0.001):
    kb.press(key)
    time.sleep(delay)

def releaseKey(key, delay=0.001):
    kb.release(key)
    time.sleep(delay)

def typeKey(key, delay=0.001):
    pressKey(key, delay)
    releaseKey(key, delay)

def tauntLaugh():
    typeKey('v')
    typeKey('e')
    typeKey('l')

def tauntTaunt():
    typeKey('v')
    typeKey('e')
    typeKey('t')

def tauntJoke():
    typeKey('v')
    typeKey('e')
    typeKey('l')

def on_press(key):
    if key == keyboard.Key.shift_l:
        tauntLaugh()
    elif key == keyboard.Key.caps_lock:
        tauntTaunt()
    elif key == keyboard.KeyCode.from_char('`'):
        tauntJoke()
    elif key == keyboard.Key.f1:
        sys.exit()
        quit()

def setupListener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def loop():
    print("Starting Smite Taunts")
    print("Looking for Smite...")
    killLoop = False
    while 1:
        if processRunning("smite"):
            print("=====Smite Found!=====")
            print("[ F1 ] --> Quit")
            print("[ ` ] --> Joke")
            print("[ CAPS ] --> Taunt")
            print("[ LSHIFT ] --> Joke")
            setupListener()
            killLoop = True

        if killLoop == True:
            break

        time.sleep(1)

loop()