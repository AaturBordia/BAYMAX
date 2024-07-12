import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser
import requests
import os
import pyautogui
import psutil
import pyjokes
import cv2

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speech(audio):
    """Convert text to speech and print it."""
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def take_instructions():
    """Listen to the user's command and return the recognized text."""
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = rec.listen(source)
    try:
        print("Recognizing...")
        instruction = rec.recognize_google(audio, language='en-in')
        print(instruction)
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        speech("Say that again please...")
        return "None"
    except sr.RequestError as e:
        print(f"Request error: {e}")
        speech("Sorry, I could not process your request.")
        return "None"
    return instruction.lower()

def greetings():
    """Greet the user."""
    speech("Hello")
    speech("I am Baymax, your personal desktop companion.")

def current_time():
    """Report the current time and phase of the day."""
    time_now = datetime.datetime.now().strftime("%I:%M:%S")
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        phase = "morning"
    elif 12 <= hour < 18:
        phase = "afternoon"
    elif 18 <= hour <= 24:
        phase = "evening"
    else:
        phase = "night"
    speech(f"It's {time_now} of {phase}")

def date():
    """Report the current date in a more readable format."""
    now = datetime.datetime.now()
    # Convert month number to month name
    month_name = now.strftime("%B")
    # Format the date string
    formatted_date = now.strftime(f"Current date is {now.day} {month_name} {now.year}")
    # Use speech function to announce the date
    speech(formatted_date)


def cpu_status():
    """Report CPU usage, battery status, storage, and RAM usage."""
    usage = str(psutil.cpu_percent())
    speech(f'Current CPU usage is at {usage}%')
    battery = psutil.sensors_battery()
    speech(f"Battery remaining is {battery.percent}%")
    hdd = psutil.disk_usage('/')
    hdd_usage = round((hdd.used / hdd.total) * 100, 2)
    speech(f"Storage used in C Drive is {hdd_usage}%")
    frequency = psutil.cpu_freq()
    speech(f"Current frequency of CPU is {frequency.current} MHz")
    ram_used = psutil.virtual_memory().percent
    speech(f"RAM used is {ram_used}%")

def jokes():
    """Tell a joke."""
    speech(pyjokes.get_joke())

def screenshot():
    """Take a screenshot and save it."""
    img = pyautogui.screenshot()
    speech("By what name should I save it?")
    file_name = take_instructions()  # Consistent with function name
    if file_name.lower() == "none" or not file_name:
        speech("No file name provided. Screenshot not saved.")
        return
    
    # Specify the directory for saving screenshots
    screenshot_dir = "screenshot/"
    
    # Create the directory if it does not exist
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    
    file_path = os.path.join(screenshot_dir, f"{file_name}.png")
    
    try:
        img.save(file_path)
        speech(f"Screenshot saved as {file_path}")
    except Exception as e:
        speech(f"Failed to save screenshot: {e}")


def camera():
    """Capture photos using the webcam."""
    speech("Press space to take an image and escape to stop the camera")
    camera = cv2.VideoCapture(0)
    cv2.namedWindow("Camera")
    img_counter = 0
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow("Camera", frame)
        k = cv2.waitKey(1)
        if k % 256 == 27:  # ESC key
            speech("Closing camera")
            break
        elif k % 256 == 32:  # Space key
            img_name = f"camera_{img_counter}.png"
            file_path = os.path.join("camera/", img_name)
            cv2.imwrite(file_path, frame) 
            speech(f"{img_name} image taken")
            img_counter += 1
    camera.release()
    cv2.destroyAllWindows()

def wikipedia_search():
    """Search Wikipedia based on user input."""
    speech("What would you like to search for on Wikipedia?")
    query = take_instructions().strip()  # Get user input and clean it
    if not query:
        speech("You did not provide a query to search.")
        return
    
    speech("Searching...")
    try:
        result = wikipedia.summary(query, sentences=2)
        speech(result)
    except wikipedia.exceptions.DisambiguationError as e:
        speech(f"Disambiguation error: {e.options[0]}")  # Suggest the first option
    except wikipedia.exceptions.PageError:
        speech("Sorry, I could not find that page.")
    except Exception as e:
        speech(f"An error occurred: {e}")

def open_website():
    """Open a website in the browser."""
    speech("Which website should I open?")
    website = take_instructions()
    if website == "None":
        return
    webbrowser.open(f"https://{website}.com")

def google_search():
    """Perform a Google search."""
    speech("What should I search?")
    search_data = take_instructions()
    if search_data == "None":
        return
    webbrowser.open(f"https://www.google.com/search?q={search_data}")
    speech("Here is the search result")

def play_song():
    """Play a song from a specified directory."""
    songs_dir = 'music'  # Directory containing music files
    try:
        songs = os.listdir(songs_dir)
        if songs:
            os.startfile(os.path.join(songs_dir, songs[0]))
            speech("Playing the song")
        else:
            speech("No songs found in the directory")
    except FileNotFoundError:
        speech("Music directory not found")

def remember():
    """Remember a piece of information."""
    speech("What should I remember?")
    information = take_instructions()
    if information == "None":
        return
    with open('data.txt', 'w') as file:
        file.write(information)
    speech(f"You asked me to remember: {information}")

def knowing():
    """Recall a piece of information."""
    try:
        with open('data.txt', 'r') as file:
            information = file.read()
        speech(f"You asked me to remember: {information}")
    except FileNotFoundError:
        speech("No information found")

def help_command():
    """Provide help information."""
    speech("Here are the keywords for the commands you can use:")
    speech("MY INTRODUCTION to repeat my introduction")
    speech("TIME to get the current time")
    speech("DATE to get the current date")
    speech("CPU STATUS to get information about CPU usage")
    speech("JOKE to hear a joke")
    speech("SCREENSHOT to take a screenshot")
    speech("CAMERA to take photos with the webcam")
    speech("WIKIPEDIA to search Wikipedia")
    speech("OPEN WEBSITE to open a website")
    speech("SEARCH to perform a Google search")
    speech("SONG to play a song")
    speech("REMEMBER to store a piece of information")
    speech("KNOW to recall the stored information")
    speech("HELP to repeat this help message")

if __name__ == "__main__":
    greetings()
    speech("I am ready to take command")  
    speech("Say help to know all my features or continue to give a command")
    while True:
        query = take_instructions()
        if 'my introduction' in query:
            greetings()
        elif 'time' in query:
            current_time()
        elif 'date' in query:
            date()
        elif 'cpu status' in query:
            cpu_status()
        elif 'joking' in query:
            jokes()
        elif 'screenshot' in query:
            screenshot()
        elif 'camera' in query:
            camera()
        elif 'wikipedia' in query:
            wikipedia_search()
        elif 'open website' in query:
            open_website()
        elif 'search' in query:
            google_search()
        elif 'song' in query:
            play_song()
        elif 'remember' in query:
            remember()
        elif 'knowing' in query:
            knowing()
        elif 'help' in query:
            help_command()
        elif 'satisfied'in query:
            speech("I cannot deactivate until you say that you are satisfied with your care.") 
            speech("Shutting down. Have a nice day!")
            break 
        
 