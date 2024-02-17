import speech_recognition as sr

# Initialize the speech recognition engine
recognizer = sr.Recognizer()

def getUserInput(timeout=2.5):
    with sr.Microphone() as source:
        print("You: Say something...")
        audio = recognizer.listen(source, timeout=timeout)
        
    try:
        user_input = recognizer.recognize_google(audio)
        return user_input.lower()
    except sr.WaitTimeoutError:
        print("Timeout: No speech detected within the specified time.")
        return ""
    except sr.UnknownValueError:
        return ""  # Return an empty string if speech is not recognized
    except sr.RequestError as e:
        print(f"Error with the request to Google Web Speech API: {e}")
        return ""