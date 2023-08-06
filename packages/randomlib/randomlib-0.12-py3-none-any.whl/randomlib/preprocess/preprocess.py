import re
from randomlib.tokenizer import Tokenize
from importlib.resources import files
import randomlib.preprocess


class Preprocess:
    stopwords = []

    def __init__(self):
        if not Preprocess.stopwords:
            Lines = files('randomlib.preprocess').joinpath(
                'marathiStopwords.txt').read_text(encoding="utf8").split('\n')
            for line in Lines:
                Preprocess.stopwords.append(line.strip())

    def removeUrl(self, text):
        return re.sub(r"http\S+", "", text)

    def removeStopwords(self, text):
        newlist = []
        t = Tokenize()
        textlist = t.wordTokenize(text, False)
        for word in textlist:
            if word not in Preprocess.stopwords:
                newlist.append(word)
        return newlist

    def removeNondevnagari(self, line, engNum = 1):
        line = [i for i in line]
        chars = ''' क ख ग घ ङ च छ ज झ ञ ट ठ ड ढ ण त थ द ध न प फ ब भ म य र ल व र्‍ श ष स ह क़ ख़ ग़ ऩ ड़ ढ़ ऱ य़ ळ ऴ फ़ ज़ ॹ ॺ ॻ ॼ ॾ ॿ ् ऄ अ आ इ ई उ ऊ ॶ ॷ ऋ ॠ ऌ ॡ ॲ ॕ ा ि ी ु ू ॖ ॗ ृ ॄ ॢ ॣ ऍ ऎ ए ऐ ऑ ऒ ओ औ ॵ ॳ ॴ ॅ ॆ े ै ॉ ॊ ो ौ ॏ ऺ ऻ ॎ ॐ ँ ऀ ं ॱ ः ॑ ॒ ॓ ॔ ऽ ॽ , . ० १ २ ३ ४ ५ ६ ७ ८ ९ ₹ । ॥ | ॰ '''
        engNums = '''0123456789'''
        i = 0
        while i < len(line):
            if engNum == 1:
                if ((line[i] not in chars) and (line[i] not in engNums)):
                    del line[i]
                    i -= 1
                i += 1
            elif engNum == 0:
                if (line[i] not in chars):
                    del line[i]
                    i -= 1
                i += 1
            else:
                print(
                    "Please pass the correct argument. \n 1 for retaining English numbers \n 0 for not retaining English numbers")
                break
        if (line[0] == " "):
            del line[0]
        if (line[len(line)-1] == " "):
            del line[len(line)-1]
        print("".join(line))
