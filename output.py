import fugashi
tagger = fugashi.Tagger()

def tokenized(text):
    words = [word.surface for word in tagger(text)]
    return words 

def lemma_Info(text):
    for word in tagger(text):
        print(word.surface, word.feature.lemma, sep="\t")