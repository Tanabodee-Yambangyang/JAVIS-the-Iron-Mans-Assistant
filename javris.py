import speech_recognition as sr
import pyttsx3
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAPI_KEY = os.getenv('OPENAPI_KEY')
client = OpenAI(api_key=OPENAPI_KEY)

def speak_text(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
    
r = sr.Recognizer()


def record_text():
    while(1):
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                
                print("Jarvis: I'm listening")
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                print(f'You: {MyText}')
                
                return MyText
            
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occured")
            
def send_to_ChatGPT(messages, model="gpt-3.5-turbo"):
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5)
    
    print(response)
    
    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    
    return message

messages = [{"role": "user", "content": "Please act like Jarvis from Iron man."}]

print("JARVIS started...")
print("=================\n")

while(1):
    
    
    text = record_text()
    messages = [{"role": "user", "content": text}]
    response = send_to_ChatGPT(messages)
    speak_text(f"Jarvis: {response}")
    
    print(response)
    