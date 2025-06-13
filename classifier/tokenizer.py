import fugashi
from datasets import load_dataset

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
    return [word.surface for word in tagger(text) if word.surface not in stopwords]

def lemma_Info(text):
    for word in tagger(text):
        print(word.surface, word.feature.lemma, sep="\t")