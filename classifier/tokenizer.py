import fugashi
from datasets import load_dataset
import spacy
 
nlp = spacy.load("ja_ginza")
dataset =load_dataset("taishi-i/nagisa_stopwords")
stopwords = dataset["nagisa_stopwords"]["words"]
tagger = fugashi.Tagger()

# def tokenize(text):
#     words = [word.surface for word in tagger(text)]
#     for word in words:
#         if word in stopwords:
#             words.remove(word)  
#     return words 

def tokenize(text):
    doc = nlp(text)
    return [token.text for token in doc if not token.is_punct]


def lemma_Info(text):
    for word in tagger(text):
        print(word.surface, word.feature.lemma, sep="\t")