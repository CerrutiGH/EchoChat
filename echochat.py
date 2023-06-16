import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
import openai
from ttkthemes import ThemedStyle
import pyttsx3
from googletrans import Translator

# Define sua chave de API
openai.api_key = ''

# Função para converter o áudio em texto usando o SpeechRecognition
def speech_to_text():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Diga algo...")
        audio = recognizer.listen(source)
        
    try:
        text = recognizer.recognize_google(audio, language='pt-BR')
        get_response(text)
    except sr.UnknownValueError:
        print("Não foi possível reconhecer a fala.")
    except sr.RequestError as e:
        print(f"Ocorreu um erro durante o reconhecimento de fala: {e}")




# Função para enviar a pergunta à API e obter a resposta
def get_response(text):
    question = text
    
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=question,
        max_tokens=1000
    )
    
    answer = response.choices[0].text.strip()
    translated_answer = translate_text(answer)
    text_to_speech(translated_answer)


def translate_text(text):
    translator = Translator()
    translation = translator.translate(text, dest='pt')
    translated_text = translation.text
    return translated_text

def text_to_speech(answer):
    engine = pyttsx3.init('sapi5')

    # Configura a voz para português (Brasil)
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_PT-BR_MARIA_11.0')
    engine.setProperty('rate', 200)
    engine.setProperty('volume', 0.8)
    

    # Sintetiza e reproduz a fala
    engine.say(answer)
    engine.runAndWait()



# Cria a janela principal
window = tk.Tk()
window.title('EchoChat')

# Aplica um tema moderno à janela
style = ThemedStyle(window)
style.set_theme('arc')  # Escolha um tema entre 'arc', 'plastik', 'equilux', etc.

# Cria os widgets da interface

speech_button = ttk.Button(window, text='Falar', command=speech_to_text)
speech_button.pack()

# Inicia o loop da interface gráfica
window.mainloop()