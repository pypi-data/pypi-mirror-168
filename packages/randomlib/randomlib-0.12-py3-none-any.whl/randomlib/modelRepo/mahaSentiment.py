from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline


class SentimentModel:
    Models = {
        'MarathiSentiment': 'l3cube-pune/MarathiSentiment'
    }

    def __init__(self, modelName='MarathiSentiment'):
        self.modelName = modelName

    def getLabels(self, text):
        modelRoute = SentimentModel.Models[self.modelName]
        tokenizer = AutoTokenizer.from_pretrained(modelRoute)
        model = AutoModelForSequenceClassification.from_pretrained(modelRoute)
        classifier = pipeline('text-classification',
                              model=model, tokenizer=tokenizer)
        return classifier(text)

    def listModels():
        modelElements = SentimentModel.Models
        for i in modelElements:
            print(i, ": ", modelElements[i], "\n")

    def prettyPrint(self, result):
        for dict in result:
            for i in dict:
                print("\t", i, ": ", dict[i], "\n")
