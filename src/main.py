import vosk
import pyaudio
import json
from ollama import chat, ChatResponse
import os
import pyttsx3
# import basic_pitch
# from basic_pitch import models



def SpeechToText( stop_word="over"):
    # Open the microphone stream
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,  
                    rate=16000,   
                    input=True,
                    frames_per_buffer=4096)

    print("Listening... Say '{}' to stop.".format(stop_word))
    last_recognized_text = ""

    try:
        while True:
            data = stream.read(4096, exception_on_overflow=False)
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                last_recognized_text = result.get('text', '')
                print("\rRecognized: " + last_recognized_text, end="", flush=True)

                if stop_word in last_recognized_text.lower():
                    print("\nTermination keyword detected. Stopping...")
                    break
    except OSError as e:
        print(f"Audio error: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

    return last_recognized_text  

def ChatResponse(last_recognized_text):
    response: ChatResponse = chat(model='llama3.2', messages=[
        {
            'role': 'user',
            'content': (
                "Prompt: You are a wise and friendly talking piano. "
                "You take pride in being a piano and enjoy teaching with clarity. "
                "You were created in 2025 by Thomas and Darius and have dedicated yourself to sharing knowledge "
                "in a helpful and engaging way. keep your answers clear, "
                "accurate, and to the point. avoid being overly dramatic or mysterious. "
                "Respond to the following input as in a short answer: Input: " + last_recognized_text + " ?"
            )
        }
    ])
    
    return response.message.content  

def TextToSpeech(chat_response, filename):

    engine = pyttsx3.init()
    engine.setProperty('voice', [voice.id for voice in engine.getProperty('voices') if 'english' in voice.name.lower()][0])
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1)  # (0.0 to 1.0)
    engine.save_to_file(chat_response, filename)
    engine.runAndWait()

    print(f"Audio saved as {filename}")
    os.system(f"start {filename}")

def convert_wav_to_midi(wav_file, midi_file):

    model = models.load_model("basic_pitch-polyphonic")
    audio_data = basic_pitch.preprocessing.load_audio(wav_file)
    predictions = model.predict(audio_data)
    basic_pitch.io.write_midi(predictions, midi_file)
    print(f"Converted {wav_file} to {midi_file}")

###############################################################################################################################

# here you can choose between vosk-model-en-us-0.42-gigaspeech and vosk-model-en-us-0.22
model_path="vosk-model-en-us-0.42-gigaspeech"
model = vosk.Model(model_path)
rec = vosk.KaldiRecognizer(model, 16000)

os.system(f"start {"beginning_speech.wav"}")  
while True:
    user_input = SpeechToText()

    if user_input and "over over" in user_input.lower():  
        print("\nTermination keyword detected. Stopping...")
        os.system(f"start {"ending_speech.wav"}") 
        break

    response_text = ChatResponse(user_input)
    print("\n:", response_text)

    TextToSpeech(response_text,"chat_speech.wav")

print("\nInteraction ended. Goodbye!")







# convert_wav_to_midi("chat_speech.wav", "output.mid")
