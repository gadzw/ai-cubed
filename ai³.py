import g4f
import os
import playsound
import asyncio
import edge_tts
import time
import speech_recognition as sr

from playsound import playsound


r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)


##########################################################################################################

g4f.debug.logging = True  
g4f.check_version = False  
from g4f.Provider import (
    You,
)


response = g4f.ChatCompletion.create(
    model=g4f.models.text_davinci_003,
    provider=g4f.Provider.You,
    messages=[{"role": "user", "content": r.recognize_google(audio, language="es-CL")}],
    
) 

##########################################################################################################
TEXT = str(response)
VOICE = "es-US-PalomaNeural"
OUTPUT_FILE = "sound.mp3"


async def amain() -> None:
    """Main function"""
    communicate = edge_tts.Communicate(TEXT, VOICE)
    with open(OUTPUT_FILE, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        loop.run_until_complete(amain())
    finally:
        loop.close()

playsound(r"C:\Users\Monica\Desktop\GADDD\sound.mp3")
os.remove(r"C:\Users\Monica\Desktop\GADDD\sound.mp3")