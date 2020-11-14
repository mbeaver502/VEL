import os
import subprocess
import psutil
from time import sleep
from pynput import keyboard
import sys
import winreg

def start_smite():
    """Starts Smite from Steam by using Steam app ID (386360).
    """

    REG_PATH = r"Software\VEL"
    def set_registry_key(name, value):
        """Sets registry name to value in HKEY_CURRENT_USER\REG_PATH.

        Args:
            name (string): Name of the registry key.
            value (string): The value of the registry key.

        Returns:
            bool: Returns True if sets the registry key, False otherwise
        """
        try:
            winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0,
                                        winreg.KEY_WRITE)
            winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
            winreg.CloseKey(registry_key)
            return True
        except WindowsError:
            return False

    def get_registry_key(name):
        """Gets the value of the registry key in HKEY_CURRENT_USER\REG_PATH

        Args:
            name (string): The name of the registry key to get.

        Returns:
            string: Returns the value of the registry key.
        """
        try:
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0,
                                        winreg.KEY_READ)
            value, regtype = winreg.QueryValueEx(registry_key, name)
            winreg.CloseKey(registry_key)
            return value
        except WindowsError:
            return None

    # https://stackoverflow.com/a/1724723
    def find(name, path):
        """Gets the path for a  file.

        Args:
            name (string): The name of the file.
            path (string): The path of the drive.

        Returns:
            string: The full path for the file.
        """
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)

    path_registry = get_registry_key("PATH")
    applaunch = ' -applaunch 386360'
    if path_registry != None:
        path_registry += applaunch
        subprocess.call(path_registry)

    default_path = r'C:\Program Files (x86)\Steam\steam.exe'

    if os.path.isfile(default_path):
        print('Trying default Steam location:', default_path)
        set_registry_key("PATH", default_path)
        subprocess.run(default_path + applaunch)
    else:
        print('Steam not found in default location...')

    drive_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    drives = ['{}:'.format(drive) for drive in drive_letters if os.path.exists('{}:'.format(drive))]

    print('Searching for Steam...')
    for drive in drives:
        path = find('steam.exe', drive)
        if path != None:
            print('Found a Steam installation:', path)
            path = path + applaunch
            set_registry_key("PATH", path)

            print('Launching SMITE:', path)
            subprocess.call(path)
            break

def smite_running():
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
def key_down(key, delay=0.001):
    """Presses a key down.

    Args:
        key (int): The keycode of the key to press.
        delay (float, optional): Time to sleep after key press. Defaults to 0.001 (1ms).
    """
    kb.type(key)
    sleep(delay)

def key_up(key, delay=0.001):
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
    key_down(key, delay)
    key_up(key, delay)

def taunt_laugh():
    """Types the keys [VEL] for laugh taunt.
    """
    type('v')
    type('e')
    type('l')

def taunt_taunt():
    """Types the keys [VET] for taunt taunt.
    """
    type('v')
    type('e')
    type('t')

def taunt_joke():
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
        taunt_laugh()
    elif key == keyboard.Key.caps_lock:
        taunt_taunt()
    elif key == keyboard.KeyCode.from_char('`'):
        taunt_joke()
    elif key == keyboard.Key.f1:
        sys.exit()
        quit()

def setup_listener():
    """Setups keyboard listener in separate thread.
    """
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def main():
    """Main Loop. Will start Smite if not launched. If Smite is already launched, keyboard listener will start.
    """
    print('VEL Smite Taunts Started!')
    if not smite_running():
        start_smite()
        print('Starting Smite...')
        while not smite_running():
            sleep(1)
        print('Smite Started!')

    print('===== Controls =====')
    print('[ F1 ]     ----> Quit')
    print('[ ` ]      ----> Joke')
    print('[ CAPS ]   ----> Taunt')
    print('[ LSHIFT ] ----> Joke')
    setup_listener()

main()