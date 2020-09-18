# main.py
# name to be changed to init.py


# import evaluation
import codeRunner
import loader as loader

# import dataPreprocessing as dp
''
'''
from nltk import word_tokenize, pos_tag, RegexpParser
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
'''

# import string as ss
# import pandas as pd
# import os


# Coderunner


'''
#######################################################
# run order
1. Loader(load resources)
2. CodeRunner(fire a single query)
3. Testing(coderunner batch search)

Common shared resources
1. complete database//(not always required)
2. processed database
3. inversed index database
#######################################################
'''

# preprocessing text data

# ################################
# it overwrites the old metadata
# dp.create_metadata()
# dp.automate_metadata_creation_offline()
# this is for demonstration purpose only


# load common shared resources
document_metadata, inverse_index, doc = loader.loadResources()


# coderunner

codeRunner.load_metadata(doc, inverse_index, document_metadata)
codeRunner.run()


# testing
# import evaluation
# evaluation.load_metadata(doc, inverse_index, document_metadata)
# evaluation.batchtestRun()


'''
# testing/ evaluation
to- do
1. automate document creation -/
2. update document metadata by adding to it "not overwriting on it" -/
3. create sample user queries -/
    for - comparision of normal and synonyms -/
        - evaluation of not, and ,or XX
        - (add if anything strikes)
4. evaluation & screenshots -/
5. precision and recall metrics -/
    -Graph if required -/
6. UI //if possible xx





'''
