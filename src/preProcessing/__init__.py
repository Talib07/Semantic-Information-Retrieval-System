# preProcessing.py
'''
To-do list
1. codereview lemmatization part
2. add hypernyms ,homonyms  and  hyponyms
3. add some  more  preprocessing functions if necessary
'''

from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer

import string as ss


def get_wordnet_pos(tag):
    # tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {
        "J": wordnet.ADJ,
        "N": wordnet.NOUN,
        "V": wordnet.VERB,
        "R": wordnet.ADV
    }
    return tag_dict.get(tag[0].upper(), wordnet.NOUN)


def getSynonyms(lemmatized_keywords):
    synns = []
    synns.extend(lemmatized_keywords)
    for word in lemmatized_keywords:
        synnonyms = []
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                synnonyms.append(l.name())
        synns.extend(synnonyms)
    synns = list(set(synns))
    synns_ex = []
    for word in synns:
        synns_ex.extend(word.split('_'))
    return (synns_ex)


def getLemmatizedKeywords(tokens):
    tokens = [key.lower() for key in tokens]
    tagged_tokens = pos_tag(tokens)
    lemmatizer = WordNetLemmatizer()

    #######code review##########
    lemmatized_keywords = []
    stop_words = set(stopwords.words('english'))

    for t in tagged_tokens:
        # ignoring stopwords and punctuation
        if t[0] not in stop_words and t[0] not in ss.punctuation:
            lemmatized_keywords.append(
                lemmatizer.lemmatize(t[0], get_wordnet_pos(t[1])))
    return (lemmatized_keywords)


# publilc functions
#######################################################################
def getFilteredKeywords(query):
    translator = str.maketrans(ss.punctuation, ' ' * len(ss.punctuation))
    query = query.translate(translator)

    tokens = word_tokenize(query)
    tokens = [key.lower() for key in tokens]

    stop_words = set(stopwords.words('english'))
    filtered_keywords = [key for key in tokens if key not in stop_words]
    return (filtered_keywords)


def getPreprocessedKeywordsWithSynonyms(query):
    query = query.lower()
    lemmatized_keywords = getPreprocessedKeywords(query)
    synonyms = getSynonyms(lemmatized_keywords)
    return (synonyms)


def getSynnsforDemonstration(query):
    def synset(word):
        synonyms = []
        for syn in wordnet.synsets(word):
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

    def expand(keywords):
        expanded_list = []
        for word in keywords:
            expanded_list.append(synset(word))
        return (expanded_list)

    def lemmatize(keywords):
        lemmatizer = WordNetLemmatizer()
        # stop_words = set(stopwords.words('english'))
        lemmatized_keywords = []
        for word in keywords:
            lemmatized_keywords.append(
                lemmatizer.lemmatize(word[0], get_wordnet_pos(word[1])))
        return lemmatized_keywords

    def clean2(keywords):
        stop_words = set(stopwords.words('english'))
        filtered = []
        for word in keywords:
            if word[0] == 'using':
                continue
            if word[0] not in ss.punctuation and word[0] not in stop_words:
                filtered.append(word[0].lower())
        return (filtered)

    def clean(keywords):
        lmkey = lemmatize(keywords)
        filtered = []
        stop_words = set(stopwords.words('english'))
        for word in lmkey:
            if word == 'use':
                continue
            if word not in ss.punctuation and word not in stop_words:
                filtered.append(word.lower())
        return (filtered)

    # tokens = word_tokenize(query)
    # print("\nTokens\t\t:",tokens)
    # tagged = pos_tag(tokens)
    # print("\nTagged\t\t:",tagged)
    # lem_allList2 = clean2(tagged)
    # lem_allList = clean(tagged)
    # print("\nLemmatized\t: ",lem_allList)
    # ext_allList = expand(lem_allList2)
    # print("\nSynonyms\n",'-'*10)
    # for e in range(len(ext_allList)):
    #     print(lem_allList[e]," \t- ",ext_allList[e])

    tokens = word_tokenize(query)
    # print("After Tokenization\n", "-"*10)
    print("Tokens\t\t:", tokens)
    tagged = pos_tag(tokens)
    # print("\nAfter POS tagging\n", "-"*10)
    print("Tagged\t\t:", tagged)
    lem_allList2 = clean2(tagged)
    lem_allList = clean(tagged)
    # print("\nAfter lemmatization and stopword removal\n", "-"*10)
    # print("Lemmatized\t: ", lem_allList)
    ext_allList = expand(lem_allList2)
    # # print("\nAfter keywords expansion\n", '-'*10)
    for e in range(len(ext_allList)):
         print("\n",lem_allList[e], "    \t- ", ext_allList[e])


def getPreprocessedKeywords(query):
    original_query = (query + '.')[:-1]

    tokens = original_query.split()
    tokens = [key.lower() for key in tokens]

    lemmatized_keywords = getLemmatizedKeywords(tokens)
    return (lemmatized_keywords)
