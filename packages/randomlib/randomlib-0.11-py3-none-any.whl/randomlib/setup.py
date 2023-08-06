# VARIABLES
languages = {
    "mr": "Marathi",
    "eng": "English",
}
code = 'mr'
BASE_DIR = 'l3cube-pune/'
MAHA_NER_BERT = BASE_DIR + "marathi-ner"
MAHA_BERT_V2 = BASE_DIR + "marathi-bert-v2"


def setup(languagecode: str):
    global code
    if languagecode in languages.keys():
        code = languagecode
    else:
        code = "mr"
    print(f"{languages[code]} Langauge set!")
