import os
from gtts import gTTS
from playsound import playsound
from googletrans import Translator

trans=Translator()

src="This is a test sentence."

ksrc=trans.translate(src,dest="kn")
tsrc=trans.translate(src,dest="te")
hsrc=trans.translate(src,dest="hi")

print("Translated sentences in Kannada,Telugu and Hindi are:")
print(ksrc.text)
print(tsrc.text)
print(hsrc.text)

kl="kn"
tl="te"
hl="hi"

obj1=gTTS(text=ksrc.text,lang=kl,slow=False)
obj1.save("kannada.mp3")
print("Converted sentence will play in Kannada now")
playsound("C:\\Users\\Karthik\\Desktop\\AYES\\kannada.mp3")


obj2=gTTS(text=tsrc.text,lang=tl,slow=False)
obj2.save("telugu.mp3")
print("Converted sentence will play in Telugu now")
playsound("C:\\Users\\Karthik\\Desktop\\AYES\\telugu.mp3")

obj3=gTTS(text=hsrc.text,lang=hl,slow=False)
obj3.save("hindi.mp3")
print("Converted sentence will play in Hindi now")
playsound("C:\\Users\\Karthik\\Desktop\\AYES\\hindi.mp3")

