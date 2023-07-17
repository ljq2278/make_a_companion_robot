from evdev import InputDevice, categorize, ecodes, KeyEvent
import requests, copy
from lib.draw_txt import draw_text, clear_text

# Find the correct event number for your USB keyboard in /dev/input
dev = InputDevice('/dev/input/event6')

# Grab the device to restrict it to this process only
dev.grab()

# Buffer to store keyboard inputs
buffer = []

# Track the state of the 'Shift' key
shift_pressed = False

# Map keys to characters
KEY_MAPPING_n = {
    'KEY_A': 'a', 'KEY_B': 'b', 'KEY_C': 'c', 'KEY_D': 'd', 'KEY_E': 'e',
    'KEY_F': 'f', 'KEY_G': 'g', 'KEY_H': 'h', 'KEY_I': 'i', 'KEY_J': 'j',
    'KEY_K': 'k', 'KEY_L': 'l', 'KEY_M': 'm', 'KEY_N': 'n', 'KEY_O': 'o',
    'KEY_P': 'p', 'KEY_Q': 'q', 'KEY_R': 'r', 'KEY_S': 's', 'KEY_T': 't',
    'KEY_U': 'u', 'KEY_V': 'v', 'KEY_W': 'w', 'KEY_X': 'x', 'KEY_Y': 'y',
    'KEY_Z': 'z',
    'KEY_SPACE': ' '
    # Add more keys as needed
}
KEY_MAPPING_sp1 = {
    'KEY_1': '1', 'KEY_2': '2', 'KEY_3': '3', 'KEY_4': '4', 'KEY_5': '5',
    'KEY_6': '6', 'KEY_7': '7', 'KEY_8': '8', 'KEY_9': '9', 'KEY_0': '0',
    'KEY_SLASH': '/', 'KEY_DOT': '.', 'KEY_COMMA': ',', 'KEY_APOSTROPHE': "'",
    'KEY_GRAVE': '`', 'KEY_MINUS': '-', 'KEY_EQUAL': '=', 'KEY_LEFTBRACE': '[', 'KEY_RIGHTBRACE': ']',
    'KEY_BACKSLASH': '\\', 'KEY_SEMICOLON': ';',
    'KEY_BACKSPACE': '',
    # Add more keys as needed
}
KEY_MAPPING_sp2 = {
    'KEY_1': '!', 'KEY_2': '@', 'KEY_3': '#', 'KEY_4': '$', 'KEY_5': '%',
    'KEY_6': '^', 'KEY_7': '&', 'KEY_8': '*', 'KEY_9': '(', 'KEY_0': ')',
    'KEY_SLASH': '?', 'KEY_DOT': '>', 'KEY_COMMA': '<', 'KEY_APOSTROPHE': '"',
    'KEY_GRAVE': '~', 'KEY_MINUS': '_', 'KEY_EQUAL': '+', 'KEY_LEFTBRACE': '{', 'KEY_RIGHTBRACE': '}',
    'KEY_BACKSLASH': '|', 'KEY_SEMICOLON': ':',
    'KEY_BACKSPACE': '',
    # Add more keys as needed
}
KEY_MAPPING = copy.deepcopy(KEY_MAPPING_n)
KEY_MAPPING.update(KEY_MAPPING_sp1)

for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        key_event = categorize(event)
        if key_event.keystate == KeyEvent.key_down:
            if key_event.keycode == 'KEY_ENTER':
                # When the Enter key is pressed, send the buffer to the server
                text = ''.join(buffer)
                print('Sending:', text)

                response = requests.post('http://192.168.1.9:8004/keyborad/', data={'text': text})
                print('Response:', response.status_code, response.text)
                # Clear the buffer
                buffer.clear()
                clear_text()
            elif key_event.keycode in ['KEY_LEFTSHIFT', 'KEY_RIGHTSHIFT']:
                # The 'Shift' key was pressed
                shift_pressed = True
            else:
                # When a key is pressed, append it to the buffer
                char = KEY_MAPPING.get(key_event.keycode, 'null')  # If the key is not in the mapping, ignore it
                if shift_pressed:
                    if key_event.keycode in KEY_MAPPING_n.keys():
                        char = char.upper()  # Convert to upper case if the 'Shift' key is pressed
                    elif key_event.keycode in KEY_MAPPING_sp2.keys():
                        char = KEY_MAPPING_sp2[key_event.keycode]
                if len(char) <= 1:
                    if len(char) == 1:
                        buffer.append(char)
                    else:
                        if len(buffer) > 0:
                            buffer.pop(-1)
                    draw_text(char)
        elif key_event.keystate == KeyEvent.key_up and key_event.keycode in ['KEY_LEFTSHIFT', 'KEY_RIGHTSHIFT']:
            # The 'Shift' key was released
            shift_pressed = False
