import dataPreprocessing as dp
import loader as loader
import pandas as pd
import os

df = loader.loadDocumentMetadata()

# print(df.columns)
import loader as loader


#df = loader.loadDocumentMetadata()
#print(df.shape)
dp.automate_metadata_creation_online("article_title","machine learning","machine learning")

path = os.getcwd()  #
meta = os.path.join(path, "resources", "auto_document_metadata.pkl")  #
metapath = meta.replace(os.sep, "/")
document_metadata = pd.read_pickle(metapath)
print(document_metadata.shape)
