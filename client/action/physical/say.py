import pyttsx3

# Initialize the pyttsx3 engine
engine = pyttsx3.init()
engine.setProperty('voice', 'english_rp+f3')

engine.setProperty('rate', 120)  # lower than 200


# Convert the text to speech

def read_alound_and_show_text(txt):
    # Create TFT LCD display class.
    if txt == "":
        txt = "Oop, it seem that I dont know what to say ! "
    print(txt)
    engine.say(txt)
    # Run the engine
    engine.runAndWait()


if __name__ == '__main__':
    read_alound_and_show_text("hello")
    # read_alound_and_show_text("Here are some ttf font Examples. Here are some ttf font Examples. Here are some ttf font Examples. Here are some ttf font Examples. ")
