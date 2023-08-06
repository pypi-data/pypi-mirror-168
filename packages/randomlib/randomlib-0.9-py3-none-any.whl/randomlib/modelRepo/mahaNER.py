from transformers import BertTokenizerFast, BertForTokenClassification, TokenClassificationPipeline
import torch
import logging
import pandas as pd
from randomlib import setup
from pprint import pprint
from randomlib.tokenizer import Tokenize
# get_labels(): sentence
# get_tokenlabel(): per token label dictionary
'''

pretrained MahaBERT Model finetuned on MahaNER Dataset = mahaNER_BERT system

'''
'''
Use BertForTokenClassification instead of TFBertForTokenClassification
Use huggingface APIs
huggingface pipeline: https://huggingface.co/docs/transformers/quicktour
use numpy
test it on punctauted statements
mode_repo will host all models
for multiple versions of models, user can specify the model (s)/he wants
1.mahaSent 2.maskmodel(mahabertv2) 3.hatespeech model 4.mahagpt
2nd group : i.sentiment, ii.tag package
ner tagger
'''


nerPipeLogger = logging.getLogger(__name__)
consoleHandler = logging.StreamHandler()
logFormatter = logging.Formatter(
    fmt=' %(name)s :: %(levelname)-4s :: %(message)s')

nerPipeLogger.setLevel(logging.DEBUG)
consoleHandler.setLevel(logging.DEBUG)

consoleHandler.setFormatter(logFormatter)
nerPipeLogger.addHandler(consoleHandler)

#logging.disable(level = "CRITICAL")


def NERPipeline(text, gpu_enabled=False):
    '''
    :param text:str/list[str] input text or list of texts
    :param gpu_enabled: set it as true if gpu present on system
    :return:List[dict] output of ner on each word in given 'text'
    '''
    device = 1 if (gpu_enabled and torch.cuda.is_available()) else -1

    model_name = setup.MAHA_NER_BERT

    try:
        assert isinstance(model_name, str) == True
    except:
        nerPipeLogger.error(
            f"model_name attribute not initialized correctly. Requires 'str' but got '{model_name}'")
        return None
    try:
        model = BertForTokenClassification.from_pretrained(model_name)
    except Exception as e:
        nerPipeLogger.exception(
            msg="some error has occured while Loading mahaNER_BERT Model", exc_info=e)
        return None
    try:
        nerTokenizer = BertTokenizerFast.from_pretrained(model_name)
    except Exception as e:
        nerPipeLogger.exception(
            msg="some error has occured while Loading mahaNER_BERT Tokenizer", exc_info=e)
        return None

    pipeline = TokenClassificationPipeline(
        model=model,
        tokenizer=nerTokenizer,
        device=device,
        framework="pt",
        task='marathi-ner',
        aggregation_strategy='average'
    )
    nerPipeLogger.info("Pipeline created")
    return pipeline(text)


def print_prediction(predictions, details: str = "minimum", as_dataframe: bool = False):
    """
       Utility function to print results of prediction.

       :param predictions: Results returned by BertTokenClassification pipeline() .
       :param details: Defines the level of details to print. Possible values: minimum, medium, all.
       :param as_dataframe: Returns result as a pandas dataframe.
       :return: None

    """
    predicts = pd.DataFrame(predictions)

    if details == 'minimum':
        result = predicts[['word', 'entity_group']]

    if details == "medium":
        result = predicts[['word', 'entity_group', 'score']]

    if details == "all":
        result = predicts

    pprint(result)

# class MarathiNER2:
#     def __init__(self, gpu_enabled=False):
#         self.model_name = setup.MAHA_NER_BERT
#         self.lang = setup.code

#         self.device = 1 if (gpu_enabled and torch.cuda.is_available()) else -1

#         self.model = BertForTokenClassification.from_pretrained(self.model_name)
#         self.nerTokenizer = BertTokenizerFast.from_pretrained(self.model_name)
#         self.pipeline = TokenClassificationPipeline(
#             model=self.model,
#             tokenizer=self.nerTokenizer,
#             device=self.device,
#             framework="pt",
#             task='marathi-ner',
#             aggregation_strategy='average'
#         )

#         self.wordTokenizer = Tokenize(setup.code)
#         self.output = None

#     def predict(self,text:str):
#         return self.pipeline(text)

#     def print_prediction(self, predictions: np.ndarray, details: str = "minimum", as_dataframe: bool = False):
#         """
#            Utility function to print results of prediction.

#            :param predictions: Results returned by BertTokenClassification predict() function.
#            :param details: Defines the level of details to print. Possible values: minimum, medium, all.
#            :param as_dataframe: Returns result as a pandas dataframe.
#            :return: None

#         """
#         predicted_token_class_ids = tf.math.argmax(predictions, axis=1)

#         predicted_tokens_classes = [self.model.config.id2label[ix] for ix in predicted_token_class_ids.numpy().tolist()]
#         result = []

#         if details == "minimum":
#             for word, class_label in zip(self.word_and_encoding_index.keys(), predicted_tokens_classes):
#                 result.append({"word": word, "label": class_label})

#         if details == "medium":
#             scores = [predictions[i][predicted_token_class_ids[i]] for i in range(len(predicted_token_class_ids))]

#             for word, class_label, score in zip(self.word_and_encoding_index.keys(), predicted_tokens_classes, scores):
#                 result.append({"word": word, "label": class_label, "score": score})

#         if as_dataframe:
#             print(pd.DataFrame(result))
#             return

#         pprint(result)
