# import loader as loader
# import retrieval as retriever
# import preProcessing as preProcessor

from nltk import word_tokenize, pos_tag, RegexpParser
#from collections import OrderedDict
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer

import string as ss


def load_metadata(doc_G, inverse_index_G, document_metadata_G):
    global doc
    global inverse_index
    global document_metadata

    doc = doc_G
    inverse_index = inverse_index_G
    document_metadata = document_metadata_G


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

    # cc_and=['and']
    # cc_or=['or']
    # neg = ['without','except']
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
                if tups[1] == 'IN' and (tups[0] == 'without'
                                        or tups[0] == 'except'):
                    for s in subtree.subtrees():
                        if s.label() == 'ENT':
                            for x in s.leaves():
                                excludeList.append(x)

    return (orList, andList, excludeList, allList)


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
        lemmatized_keywords.append(
            lemmatizer.lemmatize(word[0], get_wordnet_pos(word[1])))
    return lemmatized_keywords


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
    # print(synns)
    # print(synns_ex)
    # return (synns_ex)
    return (synns_ex)


def clean(keywords):
    lmkey = lemmatize(keywords)
    filtered = []
    stop_words = set(stopwords.words('english'))
    for word in lmkey:
        if word not in ss.punctuation and word not in stop_words:
            filtered.append(word.lower())
    return (filtered)


'''
def clean(keywords):
    filtered = []
    stop_words = set(stopwords.words('english'))
    for word in keywords:
        if word[0] not in ss.punctuation and word[0] not in stop_words:
            filtered.append(word[0].lower())
    return (filtered)
'''


def expand(keywords):
    expanded_list = []
    for word in keywords:
        expanded_list.append(synset(word))
    return (expanded_list)


def find_Occurance(keylist, docslist):
    outList = []
    for d in range(len(docslist)):
        outList.append([False] * len(keylist))
    for k in range(len(keylist)):
        # print(keylist[k])
        if keylist[k] not in inverse_index.index:
            continue
        dl = inverse_index.loc[keylist[k], 0]
        for d in range(len(docslist)):
            if docslist[d] not in dl:
                continue
            outList[d][k] = True
    # output = [len(keylist)]*[len(docslist)]
    return outList


def combinedScore(orList, andList, exList, allList, docslist):
    lem_orList = clean(orList)
    lem_andList = clean(andList)
    lem_exList = clean(exList)
    lem_allList = clean(allList)

    ext_orList = expand(lem_orList)
    ext_andList = expand(lem_andList)
    ext_exList = expand(lem_exList)
    ext_allList = expand(lem_allList)

    or_om = find_Occurance(lem_orList, docslist)
    and_om = find_Occurance(lem_andList, docslist)
    ex_om = find_Occurance(lem_exList, docslist)
    all_om = find_Occurance(lem_allList, docslist)

    # print(docslist)
    # print(all_om)
    ext_or_om = []
    ext_and_om = []
    ext_ex_om = []
    ext_all_om = []

    # print(ext_allList)

    for e in ext_orList:
        ext_or_om.append(find_Occurance(e, docslist))
    for e in ext_andList:
        ext_and_om.append(find_Occurance(e, docslist))
    for e in ext_exList:
        ext_ex_om.append(find_Occurance(e, docslist))
    for e in ext_allList:
        ext_all_om.append(find_Occurance(e, docslist))

    scoreMatrix = {}
    ext_scoreMatrix = {}
    combinedScoreMatrix = {}
    for d in range(len(docslist)):
        or_score = 0
        and_score = 0
        ex_score = 0
        all_score = 0
        ext_or_score = 0
        ext_and_score = 0
        ext_ex_score = 0
        ext_all_score = 0
        orf = False
        andf = False
        exf = False
        allf = False
        if len(or_om[d]) != 0:
            orf = True
            if sum(1 for x in or_om[d] if x) != 0:
                or_score = max(1 for x in or_om[d] if x)
            for e in ext_or_om:
                if sum(1 for x in e[d] if x) == 0:
                    continue
                ext_or_score = max(ext_or_score,
                                   min(1, max(1 for x in e[d] if x)))
        if len(and_om[d]) != 0:
            andf = True
            if sum(1 for x in and_om[d] if x) != 0:
                and_score = sum(1 / len(and_om) for x in and_om[d] if x)
            for e in ext_and_om:
                if sum(1 for x in e[d] if x) == 0:
                    continue
                ext_and_score += max(1 for x in e[d] if x) / len(andList)
        if len(ex_om[d]) != 0:
            exf = True
            if sum(1 for x in ex_om[d] if x) != 0:
                ex_score = sum(1 / len(ex_om) for x in ex_om[d] if x)
            for e in ext_ex_om:
                if sum(1 for x in e[d] if x) == 0:
                    continue
                ext_ex_score += max(1 for x in e[d] if x) / len(exList)
        if len(all_om[d]) != 0:
            allf = True
            if sum(1 for x in all_om[d] if x) != 0:
                all_score = sum(1 / len(all_om[d]) for x in all_om[d] if x)
            for e in ext_all_om:
                if sum(1 for x in e[d] if x) == 0:
                    continue
                ext_all_score += max(1 for x in e[d] if x) / len(allList)

        #scoreMatrix[d] = (or_score + and_score - (ex_score) + (all_score)) / 3
        scoreMatrix[docslist[d]] = (or_score + and_score - ex_score + all_score) / sum(
            1 for x in [orf, andf, exf, allf] if x)
        ext_scoreMatrix[docslist[d]] = (ext_or_score + ext_and_score -
                                        (ext_ex_score) + (ext_all_score)) / 3
        combinedScoreMatrix[docslist[d]] = scoreMatrix[docslist[d]] + \
            ext_scoreMatrix[docslist[d]] - (scoreMatrix[docslist[d]] * ext_scoreMatrix[docslist[d]])
        # combinedScoreMatrix[docslist[d]] = scoreMatrix[
        #    docslist[d]] * 0.75 + ext_scoreMatrix[docslist[d]] * 0.25
    return (scoreMatrix, combinedScoreMatrix)


def rank(query, docs_list):
    original_query = (query + '.')[:-1]
    query = word_tokenize(original_query)

    orList, andList, excludeList, allList = process_content(original_query)
    scoreMatrix, combinedScoreMatrix = combinedScore(
        orList, andList, excludeList, allList, docs_list)

    # ordered_scoreMatrix = OrderedDict()  # ordered_scoremat
    #ordered_CombinedScoreMatrix = OrderedDict()
    normalRankedList = []
    extendedRankedList = []

    for key, value in sorted(
            scoreMatrix.items(), key=lambda item: item[1], reverse=True):
        #print(docs_list[key],value,end = " ")
        if value == 0:
            continue
        normalRankedList.append(key)
        #ordered_scoreMatrix[key] = scoreMatrix[key]

    for key, value in sorted(
            combinedScoreMatrix.items(), key=lambda item: item[1],
            reverse=True):
        extendedRankedList.append(key)
        #ordered_CombinedScoreMatrix[key] = combinedScoreMatrix[key]

    # return(ordered_scoreMatrix, ordered_CombinedScoreMatrix, normalRankedList, extendedRankedList)
    return (scoreMatrix, combinedScoreMatrix, normalRankedList,
            extendedRankedList)


def show_results(ranked_list, limit, scoredict):
    if len(ranked_list) == 0:
        print("Sorry!!! No document found")
        return

    ##
    # print("Ranked list : ", ranked_list[:10], "....")
    ##
    print("\nThe top", min(limit, len(ranked_list)), "documents are :-\n")
    print("Document Index\tscore\t\t\tDocument Title")
    print("-" * 70)

    for d in range(min(len(ranked_list), limit)):
        print(ranked_list[d], "\t%.2f" % round(scoredict[ranked_list[d]], 2),
              "\t : ", doc.iloc[ranked_list[d], 0])
