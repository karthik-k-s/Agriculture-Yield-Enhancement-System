import speech_recognition as sr
from googletrans import Translator
  
'''AUDIO_FILE = ("tel.wav") 
r = sr.Recognizer() 
with sr.AudioFile(AUDIO_FILE) as source: 
    audio = r.record(source)   
  
try: 
    src=r.recognize_google(audio) 
  
except sr.UnknownValueError: 
    print("Google Speech Recognition could not understand audio") 
  
except sr.RequestError as e: 
    print("Could not request results from Google Speech Recognition service; {0}".format(e)) 

print("Converted text is:")
print(src)

trans=Translator()
dest=trans.translate(src,dest="en")

print("Translated into  English:")
print(dest.text)'''

from google.cloud import speech_v1p1beta1
import io


def sample_recognize(local_file_path):
    """
    Transcribe a short audio file with language detected from a list of possible
    languages

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """

    client = speech_v1p1beta1.SpeechClient()

    # local_file_path = 'resources/brooklyn_bridge.flac'

    # The language of the supplied audio. Even though additional languages are
    # provided by alternative_language_codes, a primary language is still required.
    language_code = "fr"

    # Specify up to 3 additional languages as possible alternative languages
    # of the supplied audio.
    alt1 = "kn"
    alt2 = "te"
    alt3 = "hi"
    alternative_language_codes = [
        alt,
        alt2,
        alt3
    ]
    config = {
        "language_code": language_code,
        "alternative_language_codes": alternative_language_codes,
    }
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)
    for result in response.results:
        # The language_code which was detected as the most likely being spoken in the audio
        print("Detected language: {}".format(result.language_code))
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))

sample_recognize("tel.wav")
