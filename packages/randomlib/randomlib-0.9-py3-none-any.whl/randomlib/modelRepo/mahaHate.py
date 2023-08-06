from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline


class HateModel:
    Models = {
        'mahahate-bert': 'l3cube-pune/mahahate-bert',
        'mahahate-multi-roberta': 'l3cube-pune/mahahate-multi-roberta'
    }

    def __init__(self, modelName='mahahate-bert'):
        self.modelName = modelName

    def getLabels(self, text):
        modelRoute = HateModel.Models[self.modelName]
        tokenizer = AutoTokenizer.from_pretrained(modelRoute)
        model = AutoModelForSequenceClassification.from_pretrained(modelRoute)
        classifier = pipeline('text-classification',
                              model=model, tokenizer=tokenizer)
        return classifier(text)

    def listModels():
        modelElements = HateModel.Models
        for i in modelElements:
            print(i, ": ", modelElements[i], "\n")

    def prettyPrint(self, result):
        for dict in result:
            for i in dict:
                print("\t", i, ": ", dict[i], "\n")
