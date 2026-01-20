import os
from gtts import gTTS
import pygame

# Initialize audio once
if not pygame.mixer.get_init():
    pygame.mixer.init()

def get_ramai_advice(temp, ph, do):
    """Returns (status, english_msg, telugu_msg, color)"""
    if do < 3.0:
        return "CRITICAL", "Oxygen is low! Start Aerators.", "ఆక్సిజన్ తక్కువగా ఉంది! ఎరేటర్లను ఆన్ చేయండి.", "red"
    elif temp > 32:
        return "WARNING", "High Temp: Reduce feed.", "వేడి ఎక్కువగా ఉంది. మేత తగ్గించండి.", "orange"
    elif ph < 7.0 or ph > 8.5:
        return "WARNING", "pH Imbalance: Check water.", "pH స్థాయిలో మార్పు ఉంది. నీటిని పరీక్షించండి.", "orange"
    else:
        return "HEALTHY", "All systems normal.", "అంతా బాగుంది.", "green"

def play_voice(text):
    filename = "alert.mp3"
    try:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        
        tts = gTTS(text=text, lang='te')
        tts.save(filename)
        
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Voice error: {e}")