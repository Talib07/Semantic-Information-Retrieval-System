
# import codeRunner
# import loader as loader
import preProcessing as preProcessor
import retrieval as retriever
import ranking as ranker


def load_metadata(doc_G, inverse_index_G, document_metadata_G):
    global doc
    global inverse_index
    global document_metadata

    doc = doc_G
    inverse_index = inverse_index_G
    document_metadata = document_metadata_G

    ranker.load_metadata(doc, inverse_index, document_metadata)


queries = ['convert natural language to sql query',
           'construction of vocabulary database for chinese language',
           'Use of text retrieval and nlp in software engineering',
           'framework for video searching in social network',
           'probabilistic ranking framework for video search',
           'Example based machine translation system',
           'ontology based information retrieval',
           'text simplification for machine translation',
           'query expansion technique for chinese name translation',
           'distributed multimedia information retrieval model using query routing']
expected_results = [[10, 0, 7, 98, 13],
                    [39, 0, 13, 7, 3],
                    [24, 21, 31, 6, 43],
                    [50, 58, 52, 53, 84],
                    [58, 50, 53, 51, 41],
                    [65, 76, 67, 52, 66],
                    [8, 30, 31, 42, 43],
                    [64, 77, 5, 68, 21],
                    [69, 60, 64, 0, 65],
                    [84, 58, 32, 97, 47]]


def batchtestRun():
    n_obtained_results = []
    e_obtained_results = []
    for query in queries:
        n, e = testRun(query)
        n_obtained_results.append(n)
        e_obtained_results.append(e)
    for l in range(len(e_obtained_results)):
        if l == 5:
            for i in range(0,101):
                if i not in e_obtained_results[l]:
                    print(i)
            #print(e_obtained_results[l])
            print(len(e_obtained_results[l]),e_obtained_results[l][:10])
    #precision, recall = metrics(expected_results, e_obtained_results)
    print(metrics(expected_results, n_obtained_results),len(n_obtained_results))
    print(metrics(expected_results, e_obtained_results),len(e_obtained_results))


def testRun(query):
    expanded_keywords = preProcessor.getPreprocessedKeywordsWithSynonyms(query)
    retrieved_docs_list = retriever.boolean_or_model(expanded_keywords, inverse_index)
    sMatrix, csMatrix, n_ranked, e_ranked = ranker.rank(query, retrieved_docs_list)
    return(n_ranked, e_ranked)


def calculate_precision_recall(expected_results, obtained_results):
    relevent_documents = set(expected_results)
    retrieved_documents = set(obtained_results)
    # precision at rank n= 5
    n = 5
    retrieved_documents_at_n = set(obtained_results[:n])
    precision = len(relevent_documents.intersection(
        retrieved_documents_at_n))/len(retrieved_documents_at_n)
    recall = len(relevent_documents.intersection(
        retrieved_documents))/len(relevent_documents)

    return(precision, recall)


def metrics(expected_results, obtained_results):
    precision = 0
    recall = 0
    for q in range(len(queries)):
        p, r = calculate_precision_recall(expected_results[q], obtained_results[q])
        precision += p
        recall += r
        print(p,r)
    precision /= len(queries)
    recall /= len(queries)
    return precision, recall
