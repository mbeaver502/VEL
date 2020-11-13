import subprocess
import psutil
from time import sleep
from pynput import keyboard
import sys

def startSmite():
    subprocess.call(r"C:\Program Files (x86)\Steam\Steam.exe -applaunch 386360")

def smiteRunning():
    for process in psutil.process_iter():
        try:
            if "smite" in process.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

kb = keyboard.Controller()
def keyDown(key, delay=0.001):
    kb.type(key)
    sleep(delay)

def keyUp(key, delay=0.001):
    kb.release(key)
    sleep(delay)

def type(key, delay=0.001):
    keyDown(key, delay)
    keyUp(key, delay)

def tauntLaugh():
    type('v')
    type('e')
    type('l')

def tauntTaunt():
    type('v')
    type('e')
    type('t')

def tauntJoke():
    type('v')
    type('e')
    type('l')

def on_type(key):
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

def main():
    print("VEL Smite Taunts Started!")
    if not smiteRunning():
        startSmite()
        print("Starting Smite...")
        while not smiteRunning():
            sleep(1)
        print("Smite Started!")

    print("===== Controls =====")
    print("[ F1 ] --> Quit")
    print("[ ` ] --> Joke")
    print("[ CAPS ] --> Taunt")
    print("[ LSHIFT ] --> Joke")
    setupListener()

main()