from nltk import word_tokenize, pos_tag, RegexpParser
from collections import OrderedDict
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer

import string as ss


def synset(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())
    synns = list(set(synonyms))
    return (synns)
keywords= ['framework','rank']
extended= []

for word in keywords:
    extended.append(synset(word))
print(extended)