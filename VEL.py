import os
import subprocess
import psutil
from time import sleep
from pynput import keyboard
import winreg
from threading import Thread
import configparser

#-------------------------------------------------
# CONSTANTS
#-------------------------------------------------
CONFIG_FILENAME = 'config.cfg'
SYSTEM_SECTION = 'SYSTEM'
DEFAULTPATH_KEY = 'DefaultPath'
STEAMPATH_KEY = 'SteamPath'
KEY_SEPARATOR = '~'

#-------------------------------------------------
# setup_steam
#-------------------------------------------------
def setup_steam() -> dict:
    """
    Loads Steam data from the CONFIG_FILENAME file.

        Returns:
            return (dict): 
                steam_found: Boolean indicating whether steam.exe has been found
                steam_path: String containing the steam.exe path, if it exists
                games_array: Array of dict objects representing game data from the CONFIG_FILENAME file
    """

    def get_steam_path(config: configparser.ConfigParser) -> (bool, str):
        """
        Loads the Steam path from CONFIG_FILENAME file or attempts to find a working path
        if none provided.

            Parameters:
                config (configparser.ConfigParser): Object representing the CONFIG_FILENAME file

            Returns:
                return (bool, str): Tuple whose values are:
                    bool: Boolean indicating whether a Steam installation path was found
                    str: String representing the Steam installation path, if it exists
        """

        def find(name: str, path: str) -> str:
            """
            Finds a given file in the filesystem, starting with path.

                Parameters:
                    name (str): Name of file to find
                    path (str): Root path to begin search

                Return:
                    return (str): Path of the file, if one exists
            """
            for root, dirs, files in os.walk(path):
                if name in files:
                    print(root)
                    return os.path.join(root, name)

        steam_path = ''
        steam_found = False

        if SYSTEM_SECTION in config:
            if STEAMPATH_KEY in config[SYSTEM_SECTION]:
                steam_path = config[SYSTEM_SECTION][STEAMPATH_KEY]
                if os.path.isfile(steam_path):
                    print('Using user-defined location:', steam_path)
                    steam_found = True
                else:
                    print('User-defined path {} does not exist!'.format(steam_path))
                    steam_found = False
            else:
                steam_found = False

            if not steam_found:
                if DEFAULTPATH_KEY in config[SYSTEM_SECTION]:
                    default_path = config[SYSTEM_SECTION][DEFAULTPATH_KEY]
                    if os.path.isfile(default_path):
                        print('Updating config to use path:', default_path)
                        steam_path = default_path
                        config[SYSTEM_SECTION][STEAMPATH_KEY] = steam_path
                        with open(CONFIG_FILENAME, 'w') as config_file:
                            config.write(config_file)
                        steam_found = True

                    else:
                        print('Steam not found in default location...')
                        
                        drive_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                        drives = ['{}:\\'.format(drive) for drive in drive_letters if os.path.exists('{}:'.format(drive))]

                        print('Searching for Steam...')
                        for drive in drives:
                            search_path = find('steam.exe', drive)
                            if search_path:
                                print('Found a Steam installation:', search_path)
                                print('Updating config to use new path:', search_path)
                                steam_path = search_path
                                config[SYSTEM_SECTION][STEAMPATH_KEY] = steam_path
                                with open(CONFIG_FILENAME, 'w') as config_file:
                                    config.write(config_file)
                                steam_found = True
                                break
        return (steam_found, steam_path)

    def get_games(config: configparser.ConfigParser) -> list:
        """
        Returns an array of game data contained in the CONFIG_FILENAME file.

            Parameters:
                config (configparser.ConfigParser): Object representing the CONFIG_FILENAME file

            Return:
                games_array (list): List of dict objects representing game data
        """
        games_array = []                        
        for section in config:
            if section != SYSTEM_SECTION and section != configparser.DEFAULTSECT:
                game_dict = dict()
                game_dict['game_name'] = section
                for key in config[section]:
                    key_val = config[section][key].strip()
                    if key_val:
                        game_dict[key] = key_val.split(KEY_SEPARATOR) if KEY_SEPARATOR in key_val else key_val
                games_array.append(game_dict)

        if games_array:
            print('Found these games in config:')
            for game in games_array:
                print('{}'.format(game['game_name']))
                for val in game:
                    if val != 'game_name':
                        print('  - {} = {}'.format(val, game[val]))
        
        return games_array

    config = configparser.ConfigParser()
    config.read(CONFIG_FILENAME)

    steam_found, steam_path = get_steam_path(config)
    games_array = get_games(config)
     
    return {'steam_found': steam_found, 'steam_path':steam_path, 'games_array': games_array}

#-------------------------------------------------
# smite_running
#-------------------------------------------------
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

#-------------------------------------------------
# smite_check_thread
#-------------------------------------------------
def smite_check_thread():
    """Thread function for checking for smite's process.
    """
    while 1:
        if not smite_running():
            print('Smite is no longer running, quitting now!')
            os._exit(1)
        sleep(1)

#-------------------------------------------------
# KEYBOARD HOOK METHODS
#-------------------------------------------------
# kb is our keyboard object
kb = keyboard.Controller()

#-------------------------------------------------
# key_down
#-------------------------------------------------
def key_down(key, delay=0.001):
    """Presses a key down.

    Args:
        key (int): The keycode of the key to press.
        delay (float, optional): Time to sleep after key press. Defaults to 0.001 (1ms).
    """
    kb.type(key)
    sleep(delay)

#-------------------------------------------------
# key_up
#-------------------------------------------------
def key_up(key, delay=0.001):
    """Releases a key that is pressed.

    Args:
        key (int): The keycode of the key to press.
        delay (float, optional): Time to sleep after key release. Defaults to 0.001 (1ms).
    """
    kb.release(key)
    sleep(delay)

#-------------------------------------------------
# type
#-------------------------------------------------
def type(key, delay=0.001):
    """Simulates a single keystroke, pressing a key and releasing it.

    Args:
        key (int): The keycode of the key to press.
        delay (float, optional): Time to sleep after press and release. Defaults to 0.001 (1ms).
    """
    key_down(key, delay)
    key_up(key, delay)

#-------------------------------------------------
# taunt_laugh
#-------------------------------------------------
def taunt_laugh():
    """Types the keys [VEL] for laugh taunt.
    """
    type('v')
    type('e')
    type('l')

#-------------------------------------------------
# taunt_taunt
#-------------------------------------------------
def taunt_taunt():
    """Types the keys [VET] for taunt taunt.
    """
    type('v')
    type('e')
    type('t')

#-------------------------------------------------
# taunt_joke
#-------------------------------------------------
def taunt_joke():
    """Types the keys [VEJ] for joke taunt.
    """
    type('v')
    type('e')
    type('j')

#-------------------------------------------------
# on_press
#-------------------------------------------------
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
    elif key == keyboard.Key.f5:
        os._exit(1)

#-------------------------------------------------
# start_threads
#-------------------------------------------------
def start_threads():
    """Starts Threads
            - 1. Process Listener
            - 2. Keyboard Listener
    """
    Thread(target=smite_check_thread).start()
    keyboard.Listener(on_press=on_press).start()

#-------------------------------------------------
# main
#-------------------------------------------------
def main():
    """Main Loop. Will start Smite if not launched. If Smite is already launched, keyboard listener will start.
    """
    steam = setup_steam()
    if steam['steam_found'] and steam['games_array']:
        print('Setup successful.')
    else:
        print('Setup failed. Aborting.')
        os._exit(-1)


    # print('VEL Smite Taunts Started!')
    # if not smite_running():
    #     start_smite()
    #     print('Starting Smite...')
    #     while not smite_running():
    #         sleep(1)
    #     print('Smite Started!')
    # start_threads() 

#-------------------------------------------------
# ENTRYPOINT
#-------------------------------------------------
if __name__ == "__main__":
    main()
