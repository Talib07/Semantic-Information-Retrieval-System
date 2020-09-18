
from nltk.corpus import stopwords, wordnet
from nltk import word_tokenize, pos_tag
import string as ss


def get_wordnet_pos(tag):
    #tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {
        "J": wordnet.ADJ,
        "N": wordnet.NOUN,
        "V": wordnet.VERB,
        "R": wordnet.ADV
    }
    return tag_dict.get(tag[0].upper(), wordnet.NOUN)

def synset(word):
    synonyms = []
    for syn in wordnet.synsets(word[0]):
        if syn.pos() != get_wordnet_pos(word[1]):
            print(get_wordnet_pos(word[1]),syn.pos())
            for l in syn.lemmas():
                print(l.name())
            continue
        for l in syn.lemmas():
            synonyms.append(l.name())
    synns = list(set(synonyms))
    synns_ex = []
    for word in synns:
        ex = word.split('_')
        synns_ex.extend(ex)
    synns_ex.extend(synns)
    synns_ex = list(set(synns_ex))
    return (synns_ex)


def clean(keywords):
    filtered = []
    stop_words = set(stopwords.words('english'))
    for word in keywords:
        if word[0] not in ss.punctuation and word[0] not in stop_words:
            filtered.append(word)
    return (filtered)


def expand(keywords):
    expanded_list = []
    for word in keywords:
        expanded_list.append(synset(word))
    return (expanded_list)


query = "based"
tokens = word_tokenize(query)
tagged = pos_tag(tokens)
print(tagged)
print(expand(tagged))

