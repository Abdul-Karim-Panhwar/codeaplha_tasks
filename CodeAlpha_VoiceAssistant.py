import pyttsx3
import speech_recognition as sr
import datetime
import random

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Dictionary to store notes
notes = {}

# List to store reminders
reminders = []

# Function to transcribe from audio to text
def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None
        except Exception as e:
            print(f"Skipping unknown error: {e}")
            return None

# Function to speak the generated responses
def speak_text(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error speaking text: {e}")

# Function to add a note
def add_note():
    title = input("Enter note title: ")
    content = input("Enter note content: ")
    notes[title] = content
    speak_text(f"Note titled '{title}' added.")
    print(f"Note titled '{title}' added.")

# Function to view a note
def view_note():
    title = input("Enter note title to view: ")
    if title in notes:
        speak_text(f"Note titled '{title}' says: {notes[title]}")
        print(f"Note titled '{title}' says: {notes[title]}")
    else:
        speak_text(f"No note found with the title '{title}'.")
        print(f"No note found with the title '{title}'.")

# Function to edit a note
def edit_note():
    title = input("Enter note title to edit: ")
    if title in notes:
        content = input("Enter new note content: ")
        notes[title] = content
        speak_text(f"Note titled '{title}' updated.")
        print(f"Note titled '{title}' updated.")
    else:
        speak_text(f"No note found with the title '{title}'.")
        print(f"No note found with the title '{title}'.")

# Function to delete a note
def delete_note():
    title = input("Enter note title to delete: ")
    if title in notes:
        del notes[title]
        speak_text(f"Note titled '{title}' deleted.")
        print(f"Note titled '{title}' deleted.")
    else:
        speak_text(f"No note found with the title '{title}'.")
        print(f"No note found with the title '{title}'.")

# Function to set a reminder
def set_reminder():
    time = input("Enter reminder time (in HH:MM format): ")
    message = input("Enter reminder message: ")
    reminders.append({'time': time, 'message': message})
    speak_text(f"Reminder set for {time}.")
    print(f"Reminder set for {time}.")

# Function to tell a random fact
def tell_fact():
    facts = [
        "Honey never spoils.",
        "A group of flamingos is called a 'flamboyance'.",
        "Octopuses have three hearts.",
        "Bananas are berries, but strawberries aren't."
    ]
    fact = random.choice(facts)
    speak_text(f"Did you know? {fact}")
    print(f"Did you know? {fact}")

# Function to tell a joke
def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you call fake spaghetti? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't programmers like nature? It has too many bugs."
    ]
    joke = random.choice(jokes)
    speak_text(joke)
    print(joke)

# Function to tell the current time, date, and day of the week
def tell_time_date_day():
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M")
    date_str = now.strftime("%Y-%m-%d")
    day_str = now.strftime("%A")
    speak_text(f"Current time is {time_str}, date is {date_str}, and today is {day_str}.")
    print(f"Current time is {time_str}, date is {date_str}, and today is {day_str}.")

# Function to handle gratitude messages
def respond_to_gratitude():
    responses = [
        "You're welcome!",
        "No problem!",
        "Glad I could help!",
        "Anytime!",
        "You're very welcome!"
    ]
    response = random.choice(responses)
    speak_text(response)
    print(response)

# Function to match command and execute corresponding function
def execute_command(command):
    command = command.lower().strip()
    print(f"Debug: Processing command '{command}'")  # Debugging output

    if "add note" in command or ("note" in command and "add" in command):
        add_note()
    elif "view note" in command or ("note" in command and "view" in command):
        view_note()
    elif "edit note" in command or ("note" in command and "edit" in command):
        edit_note()
    elif "delete note" in command or ("note" in command and "delete" in command):
        delete_note()
    elif "set reminder" in command or ("reminder" in command and "set" in command):
        set_reminder()
    elif "fact" in command or "random fact" in command:
        tell_fact()
    elif "joke" in command:
        tell_joke()
    elif "time" in command or "date" in command or "day" in command:
        tell_time_date_day()
    elif "thank you" in command or "thanks" in command:
        respond_to_gratitude()
    else:
        speak_text("Sorry, I didn't understand that command.")
        print(f"Unknown command: {command}")


# Main loop
def main():
    recognizer = sr.Recognizer()
    while True:
        print("Say 'Nova' to start recording your question or command.")
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                print(f"Debug: Transcription '{transcription}'")  # Debugging output
                if transcription and transcription.lower().strip() == 'nova':
                    speak_text("What can I do for you?")
                    while True:
                        with sr.Microphone() as source:
                            print("Listening for command...")
                            audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                            filename = "input.wav"
                            with open(filename, "wb") as f:
                                f.write(audio.get_wav_data())

                        text = transcribe_audio_to_text(filename)
                        if text:
                            print(f"You said: {text}")
                            execute_command(text)
                        else:
                            speak_text("Sorry, I didn't catch that.")
                            print("No transcription returned.")
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
