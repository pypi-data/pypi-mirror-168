from randomlib import setup


class Tokenize:
    def __init__(self):
        self.lang = setup.code

    def sentenceTokenize_mr(self, txt):
        punc_for_sentence_end = '''.!?'''
        sentences = []
        string = ""
        for i in txt:
            if i not in punc_for_sentence_end:
                string += i
            else:
                string += i
                sentences.append(string)
                string = ""
        print(sentences)

    def sentenceTokenize(self, txt):
        if (self.lang == 'mr'):
            self.sentenceTokenize_mr(txt)

    def wordTokenize_mr(self, txt, punctuation):
        punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        if punctuation:
            str = ""
            tokens = []
            for ele in txt:
                if ele in punc:
                    if str:
                        tokens.append(str)
                        str = ""
                    tokens.append(ele)
                elif ele == " ":
                    if str:
                        tokens.append(str)
                        str = ""
                else:
                    str += ele
            if str:
                tokens.append(str)
                str = ""
            return tokens
        else:
            for ele in txt:
                if ele in punc:
                    txt = txt.replace(ele, " ")
            x = txt.split()
            return x

    def wordTokenize(self, line, punctuation=True):
        if (self.lang == 'mr'):
            result = self.wordTokenize_mr(line, punctuation)
            return result
