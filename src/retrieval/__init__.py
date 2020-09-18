# retrieval.py
def boolean_or_model(keywords, inverse_index_document):
    retrieved_list = set()
    for key in keywords:
        if key not in inverse_index_document.index:
            continue
        retrieved_list = retrieved_list.union(inverse_index_document.loc[key, 0])
    retrieved_list = list(retrieved_list)
    retrieved_list.sort()
    return (retrieved_list)
