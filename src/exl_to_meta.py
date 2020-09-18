import dataPreprocessing as dp
import os
import pandas as pd
# path = os.getcwd()
# doc_path = os.path.join(path, "resources", "new.xlsx")

# df = pd.read_excel(doc_path)
# #
#dp.create_metadata()
#print(df.columns)
path = os.getcwd()
dm_path = os.path.join(path, "resources", "document_metadata.pkl")  #
iid_path = os.path.join(path, "resources", "inverse_index.pkl")
document_metadata = pd.read_pickle(dm_path)
iid = pd.read_pickle(iid_path)
print(iid[0])
