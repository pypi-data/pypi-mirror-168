from randomlib.modelRepo.mahaSentiment import SentimentModel

Models = {
    'MarathiSentiment': 'l3cube-pune/MarathiSentiment'
}


def listModels():
    modelElements = Models
    print("Sentiment Analysis Models: ")
    for i in modelElements:
        print(i, ": ", modelElements[i], "\n")


listModels()
