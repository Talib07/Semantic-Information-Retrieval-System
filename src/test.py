import loader as loader
import retrieval as retriever
import preProcessing as preProcessor
# import pandas as pd
from nltk import word_tokenize, pos_tag, RegexpParser
from collections import OrderedDict
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer

import string as ss


def loadMetadata(document_metadata, inverse_index):
    global df
    global iit
    df = document_metadata
    iit = inverse_index


def process_content(query):
    # query = "information retrieval and ranking not machine learning"

    tokens = word_tokenize(query)
    tagged = pos_tag(tokens)
    # print(tagged)
    chunkGram = ''' ENT: {<DT>?<JJ>*<NN.*>+|<V.*|JJ>}
                    CNJ: {<ENT>+<CC><ENT>}
                    RBN: {<RB.*|IN><V.*>?<ENT>}
                '''

    chunkParser = RegexpParser(chunkGram)
    chunked = chunkParser.parse(tagged)

    # print(chunked)
    # chunked.draw()
    allList = []
    andList = []
    orList = []
    excludeList = []
    for subtree in chunked.subtrees():
        orBool = False
        andBool = False
        if subtree.label() == 'ENT':
            for x in subtree.leaves():
                allList.append(x)
        if subtree.label() == 'CNJ':
            for tups in subtree.leaves():
                if tups[1] == 'CC' and tups[0] == 'and':
                    andBool = True
                elif tups[1] == 'CC' and tups[0] == "or":
                    orBool = True
            for s in subtree.subtrees():
                if s.label() == 'ENT':
                    if andBool:
                        for x in s.leaves():
                            andList.append(x)
                    elif orBool:
                        for x in s.leaves():
                            orList.append(x)
        if subtree.label() == 'RBN':
            for tups in subtree.leaves():
                if tups[1] == 'RB' and tups[0] == 'not':
                    for s in subtree.subtrees():
                        if s.label() == 'ENT':
                            for x in s.leaves():
                                excludeList.append(x)
                if tups[1] == 'IN' and (tups[0] == 'without' or tups[0] == 'except'):
                    for s in subtree.subtrees():
                        if s.label() == 'ENT':
                            for x in s.leaves():
                                excludeList.append(x)

    return (orList, andList, excludeList, allList)


def orRanking(orList, docs_list):
    # orScore 1
    if len(orList) == 0:
        orScoremat = []
        for i in range(len(docs_list)):
            orScoremat.append([1])
        return (orScoremat)
    orScoremat = []
    for i in range(len(docs_list)):
        orScoremat.append([0] * len(orList))

    for kin in range(len(orList)):
        for d in range(len(docs_list)):
            if orList[kin] in df.iloc[docs_list[d], 1] or orList[kin] in df.iloc[docs_list[d], 2]:
                orScoremat[d][kin] = 1

    return (orScoremat)


def andRanking(andList, docs_list):
    if len(andList) == 0:
        andScoremat = []
        for i in range(len(docs_list)):
            andScoremat.append([1])
        return (andScoremat)
    andScore = 1 / len(andList)
    andScoremat = []
    for i in range(len(docs_list)):
        andScoremat.append([0] * len(andList))

    for kin in range(len(andList)):
        for d in range(len(docs_list)):
            if andList[kin] in df.iloc[docs_list[d], 1] or andList[kin] in df.iloc[docs_list[d], 2]:
                andScoremat[d][kin] = andScore
            # if docs_list[d] == 8:
            #     print("and",andList[kin][0])
    return (andScoremat)


def allRanking(allList, docs_list):
    # general intensity  = 0.75 # to be modified
    allScore = 1 / len(allList)
    allScoremat = []
    for i in range(len(docs_list)):
        allScoremat.append([0] * len(allList))

    for kin in range(len(allList)):
        for d in range(len(docs_list)):
            if allList[kin] in df.iloc[docs_list[d], 1] or allList[kin] in df.iloc[docs_list[d], 2]:
                allScoremat[d][kin] = allScore
            # if docs_list[d] == 8:
            #     print("a",allList[kin],allScoremat[d])

    return (allScoremat)


def excludeRanking(excList, docs_list):
    # exclude intensity  = -0.33 #to be modified
    if len(excList) == 0:
        excScoremat = []
        for i in range(len(docs_list)):
            excScoremat.append([1])
        return (excScoremat)

    excScore = -3/len(excList)

    excScoremat = []
    for i in range(len(docs_list)):
        excScoremat.append([1 / len(excList)] * len(excList))

    for kin in range(len(excList)):
        for d in range(len(docs_list)):
            if excList[kin] in df.iloc[docs_list[d], 1] or excList[kin] in df.iloc[docs_list[d], 2]:
                excScoremat[d][kin] += excScore
            # if docs_list[d] == 50:
            #     print("e", excList[kin], excScoremat[d])
            # ADD synns part

    return (excScoremat)


def scoreSum(orS, andS, allS, exlS, docs_list):
    # print(docs_list)
    scoremat = {}
    for i in range(len(docs_list)):

        scoremat[docs_list[i]] = 0
        orScore = min(1, max(orS[i]))
        andScore = sum(andS[i])
        excScore = sum(exlS[i])
        allScore = sum(allS[i])
        scoremat[docs_list[i]] += (orScore + andScore + (excScore) +
                                   (allScore)) / 4

    return (scoremat)


def synset(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())
    synns = list(set(synonyms))
    return (synns)


def get_wordnet_pos(tag):
    #tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {
        "J": wordnet.ADJ,
        "N": wordnet.NOUN,
        "V": wordnet.VERB,
        "R": wordnet.ADV
    }
    return tag_dict.get(tag[0].upper(), wordnet.NOUN)


def lemmatize(keywords):
    lemmatizer = WordNetLemmatizer()
    # stop_words = set(stopwords.words('english'))

    lemmatized_keywords = []
    for word in keywords:
        lemmatized_keywords.append(lemmatizer.lemmatize(
            word[0], get_wordnet_pos(word[1])))
    return lemmatized_keywords


def clean(keywords):
    lmkey = lemmatize(keywords)
    filtered = []
    stop_words = set(stopwords.words('english'))
    for word in lmkey:
        if word not in ss.punctuation and word not in stop_words:
            filtered.append(word)
    return(filtered)


def expand(keywords):
    expanded_list = []
    for word in keywords:
        expanded_list.append(synset(word))
    return(expanded_list)


def combinedScore(orList, andList, excludeList, allList, docs_list):
    # Add synonyms for each list
    lem_orList = clean(orList)
    lem_andList = clean(andList)
    lem_excludeList = clean(excludeList)
    lem_allList = clean(allList)

    ext_orList = expand(lem_orList)
    ext_andList = expand(lem_andList)
    ext_excludeList = expand(lem_excludeList)
    ext_allList = expand(lem_allList)

    scoreMatrix = {}
    for i in range(len(docs_list)):

        scoreMatrix[docs_list[i]] = 0
        orScore = min(1, max(orRanking(lem_orList, docs_list)[i]))
        andScore = sum(andRanking(lem_andList, docs_list)[i])
        excScore = sum(excludeRanking(lem_excludeList, docs_list)[i])
        allScore = sum(allRanking(lem_allList, docs_list)[i])
        scoreMatrix[docs_list[i]] += (orScore/2 + andScore + (excScore) + (allScore)/2) / 3
    
    
    
    # scoreMatrix = scoreSum(orRanking(lem_orList, docs_list), andRanking(lem_andList, docs_list),allRanking(lem_allList, docs_list), excludeRanking(lem_excludeList, docs_list),docs_list)

    

    extscoreMatrix = expandedScoreSum()

    ranked_list = []

    ordered_scoreMatrix = OrderedDict()  # ordered_scoremat
    for key, value in sorted(scoreMatrix.items(), key=lambda item: item[1], reverse=True):
        ranked_list.append(key)
        ordered_scoreMatrix[key] = scoreMatrix[key]

    return(scoreMatrix, ranked_list)


def ranking(query, docs_list):
    original_query = (query + '.')[:-1]
    query = word_tokenize(original_query)

    orList, andList, excludeList, allList = process_content(original_query)
    scorematrix, rankedlist = combinedScore(
        orList, andList, excludeList, allList, docs_list)
    #scorematrix, rankedlist = combinedExpandedScore(
    #    orList, andList, excludeList, allList, docs_list)
    return(scorematrix, rankedlist)


# loading the document metadata
document_metadata = loader.loadDocumentMetadata()
inverse_index = loader.loadInverseIndexedDoc()
doc = loader.loadDocuments()
# maybe a infinite loop here

# 1. Query input
print("\n")
query = input("Enter query : ")
print("\n")
original_query = (query + '.')[:-1]

# 2. query pre processing
keywords = preProcessor.getFilteredKeywords(query)
lemmatized_keywords = preProcessor.getPreprocessedKeywords(query)
expanded_keywords = preProcessor.getPreprocessedKeywordsWithSynonyms(query)

# 3. Retrieval
retrieved_docs_list = retriever.boolean_or_model(expanded_keywords,
                                                 inverse_index)

# 4. Ranking
loadMetadata(document_metadata, inverse_index)
scoreMatrix, ranked_list = ranking(query, retrieved_docs_list)


def show_results(retrieved_list, ranked_list, limit):
    if len(ranked_list) == 0:
        print("Sorry!!! No document found")
        return
    doc = loader.loadDocuments()
    ##
    print("Ranked list : ", ranked_list[:10], "....")
    ##
    print("\nThe top", min(limit, len(ranked_list)), "documents are :-\n")
    print("Document Index\t\t\t\tDocument Title")
    print("-" * 70)

    for d in range(min(len(ranked_list), limit)):
        print(ranked_list[d], "\t : ", doc.iloc[ranked_list[d], 0])


limit = 5
show_results(retrieved_docs_list, ranked_list, limit)
