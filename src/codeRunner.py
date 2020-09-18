# codeRunner.py
# import pandas as pd

import preProcessing as preProcessor
import retrieval as retriever
#import loader as loader
import ranking as ranker


def load_metadata(doc_G, inverse_index_G, document_metadata_G):
    global doc
    global inverse_index
    global document_metadata

    doc = doc_G
    inverse_index = inverse_index_G
    document_metadata = document_metadata_G

    ranker.load_metadata(doc, inverse_index, document_metadata)


def run():
    # 1. Query input
    print("\n")
    query = input("Enter query : ")
    print("\n")
    #original_query = (query + '.')[:-1]

    # 2. query pre processing
    #keywords = preProcessor.getFilteredKeywords(query)
    #lemmatized_keywords = preProcessor.getPreprocessedKeywords(query)
    expanded_keywords = preProcessor.getPreprocessedKeywordsWithSynonyms(query)
    #print(expanded_keywords)
    preProcessor.getSynnsforDemonstration(query)
    # 3. Retrieval
    retrieved_docs_list = retriever.boolean_or_model(expanded_keywords,
                                                     inverse_index)
    # print("After retrieval\n","-"*10)
    # print("Retrieved Documents list :",retrieved_docs_list)
    # 4. Ranking
    scoreMatrix, combinedScoreMatrix, normalRankedList, extendedRankedList = ranker.rank(
        query, retrieved_docs_list)
    # print("After ranking\n","-"*10)
    # print("Ranked Document list :",extendedRankedList)

    # print(scoreMatrix)
    limit = 5

    #show_results(normalRankedList, limit, scoreMatrix)

    show_results(extendedRankedList, limit, combinedScoreMatrix)


def testRun(query):
    expanded_keywords = preProcessor.getPreprocessedKeywordsWithSynonyms(query)
    retrieved_docs_list = retriever.boolean_or_model(expanded_keywords, inverse_index)
    sMatrix, csMatrix, n_ranked, e_ranked = ranker.rank(query, retrieved_docs_list)
    return(n_ranked, e_ranked)


def show_results(ranked_list, limit, scoredict):
    if len(ranked_list) == 0:
        print("Sorry!!! No document found")
        return

    ##
    # print("Ranked list : ", ranked_list[:10], "....")
    ##
    print("\nThe top", min(limit, len(ranked_list)), "documents are :-\n")
    print("Doc_Index\tscore\t\t\tDocument Title")
    print("-" * 70)

    for d in range(min(len(ranked_list), limit)):
        ext = ""
        s = str(doc.iloc[ranked_list[d], 0])
        if len(s)>=75:
            ext = "..."
        print(ranked_list[d], "\t\t%.2f" % round(scoredict[ranked_list[d]], 2),
              "\t : ", s[:75],ext)
