from randomlib.modelRepo.mahaHate import HateModel

Models = {
    'mahahate-bert': 'l3cube-pune/mahahate-bert',
    'mahahate-multi-roberta': 'l3cube-pune/mahahate-multi-roberta'
}


def listModels():
    modelElements = Models
    print("Hate Speech Models: ")
    for i in modelElements:
        print(i, ": ", modelElements[i], "\n")


listModels()
