from googletrans import Translator

class Language:
    def translate(str,l):
        trans=Translator()
        s=trans.translate(str,dest=l)
        return s
        