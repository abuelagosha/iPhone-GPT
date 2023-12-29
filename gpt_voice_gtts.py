import speech_recognition as sr
from openai import OpenAI
import os
from gtts import gTTS
from playsound import playsound

# Replace with your OpenAI API key
api_key = "###"

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=api_key)

def recognize_speech_from_mic(recognizer, microphone, timeout=120):
    """Capture speech from the microphone and convert it to text."""
    with microphone as source:
        print("Please speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=timeout)  
        # Adjust the recognizer's timeout
 
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "I couldn't understand what you said."
    except sr.RequestError:
        return "Speech service error."

def chat_with_gpt(text):
    """Interact with ChatGPT and return its response."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Replace with your preferred model
            messages=[{"role": "user", "content": text}]
        )

        # Print the full API response for debugging
        print("API Response:", response)

        # Directly extract content from the API response
        try:
            content = response.choices[0].message.content
            return content
        except Exception as extraction_error:
            print("Error extracting content:", str(extraction_error))
            return "Error extracting content."

    except Exception as e:
        return f"An error occurred: {str(e)}"

def speak_text(text, speed = 4.0):
    """Convert text to speech using gTTS and play it."""
    tts = gTTS(text=text, lang='en')
    #Adjust speed
    tts.speed = speed
    tts.save("response.mp3")
    playsound("response.mp3")
    os.remove("response.mp3")

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        input_text = recognize_speech_from_mic(recognizer, microphone)
        print("You said:", input_text)

        if input_text.lower() == "exit":
            print("Exiting...")
            break

        gpt_response = chat_with_gpt(input_text)
        print("GPT replied:", gpt_response)
        speak_text(gpt_response, speed = 4.0)

if __name__ == "__main__":
    main()
