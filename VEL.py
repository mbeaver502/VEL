import subprocess
import psutil
from time import sleep
from pynput import keyboard
import sys

def startSmite():
    """Starts Smite from Steam by using Steam app ID (386360).
    """
    subprocess.call(r"C:\Program Files (x86)\Steam\Steam.exe -applaunch 386360")

def smiteRunning():
    """Checks to see if Smite is currently running.

    Returns:
        bool: The return value. Returns True if Smite is running, False otherwise.
    """
    for process in psutil.process_iter():
        try:
            if "smite" in process.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

# kb is our keyboard object
kb = keyboard.Controller()
def keyDown(key, delay=0.001):
    """Presses a key down.

    Args:
        key (int): The keycode of the key to press.
        delay (float, optional): Time to sleep after key press. Defaults to 0.001 (1ms).
    """
    kb.type(key)
    sleep(delay)

def keyUp(key, delay=0.001):
    """Releases a key that is pressed.

    Args:
        key (int): The keycode of the key to press.
        delay (float, optional): Time to sleep after key release. Defaults to 0.001 (1ms).
    """
    kb.release(key)
    sleep(delay)

def type(key, delay=0.001):
    """Simulates a single keystroke, pressing a key and releasing it.

    Args:
        key (int): The keycode of the key to press.
        delay (float, optional): Time to sleep after press and release. Defaults to 0.001 (1ms).
    """
    keyDown(key, delay)
    keyUp(key, delay)

def tauntLaugh():
    """Types the keys [VEL] for laugh taunt.
    """
    type('v')
    type('e')
    type('l')

def tauntTaunt():
    """Types the keys [VET] for taunt taunt.
    """
    type('v')
    type('e')
    type('t')

def tauntJoke():
    """Types the keys [VEJ] for joke taunt.
    """
    type('v')
    type('e')
    type('j')

def on_press(key):
    """Callback function for our keyboard listener. Listens for a key and will carry out the following if pressed:
        - Left Shift: Laugh
        - Caps Lock: Taunt
        - Tilde: Joke
        - F1: Quit

    Args:
        key (int): The keycode of the key press to listen for.
    """
    if key == keyboard.Key.shift_l:
        tauntLaugh()
    elif key == keyboard.Key.caps_lock:
        tauntTaunt()
    elif key == keyboard.KeyCode.from_char('`'):
        tauntJoke()
    elif key == keyboard.Key.f1:
        keyboard.Listener.stop()
        sys.exit()
        quit()

def setupListener():
    """Setups keyboard listener in separate thread.
    """
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def main():
    """Main Loop. Will start Smite if not launched. If Smite is already launched, keyboard listener will start.
    """
    print("VEL Smite Taunts Started!")
    if not smiteRunning():
        startSmite()
        print("Starting Smite...")
        while not smiteRunning():
            sleep(1)
        print("Smite Started!")

    print("===== Controls =====")
    print("[ F1 ]     ----> Quit")
    print("[ ` ]      ----> Joke")
    print("[ CAPS ]   ----> Taunt")
    print("[ LSHIFT ] ----> Joke")
    setupListener()

main()