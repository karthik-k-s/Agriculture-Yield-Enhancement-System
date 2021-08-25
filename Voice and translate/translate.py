from gtts import gTTS
from playsound import playsound
  
# This module is imported so that we can  
# play the converted audio 
import os 
  
from googletrans import Translator



# The text that you want to convert to audio
translator = Translator()


kn=translator.translate("ನನ್ನ ಹೆಸರು ಕಾರ್ತಿಕ್.ಇದು ಪರೀಕ್ಷೆ")
print(kn.text)
m=kn.text

te=translator.translate("ನನ್ನ ಹೆಸರು ಕಾರ್ತಿಕ್.ಇದು ಪರೀಕ್ಷೆ",dest="te")
print(te.text)
t=te.text
  
# Language in which you want to convert 
language = 'kn'
  
# Passing the text and language to the engine,  
# here we have marked slow=False. Which tells  
# the module that the converted audio should  
# have a high speed 
myobj = gTTS(text=m, lang=language, slow=False) 
  
# Saving the converted audio in a mp3 file named 
# welcome  
myobj.save("welcome1.mp3") 
  
# Playing the converted file
#os.system("mpg321 welcome.mp3")

playsound("C:\\Users\\Karthik\\Desktop\\welcome1.mp3")



# Language in which you want to convert 
language = 'te'
  
# Passing the text and language to the engine,  
# here we have marked slow=False. Which tells  
# the module that the converted audio should  
# have a high speed 
myobj2 = gTTS(text=t, lang=language, slow=False) 
  
# Saving the converted audio in a mp3 file named 
# welcome  
myobj2.save("welcome2.mp3") 
  
# Playing the converted file
#os.system("mpg321 welcome.mp3")

playsound("C:\\Users\\Karthik\\Desktop\\welcome2.mp3")




