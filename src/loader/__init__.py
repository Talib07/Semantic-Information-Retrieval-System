###loader.py(__init__)
## Inverse_indexed_doc (iid)
## document_metadata (dm)

import pandas as pd
import os

#################################################################################
####Need to revise this part. Path should be chosen automatically not manually  #
#path = os.path.dirname(os.getcwd())  #
path = os.getcwd()
dm_path = os.path.join(path, "resources", "document_metadata.pkl")  #
iid_path = os.path.join(path, "resources", "inverse_index.pkl")  #
doc_path = os.path.join(path, "resources", "Dataset_100.xlsx")

# doc_path = os.path.join(path, "resources", "new.xlsx")
# dm_path = os.path.join(path, "resources", "auto_document_metadata.pkl")  #
# iid_path = os.path.join(path, "resources", "auto_inverse_index.pkl")  #

auto_dm_path = os.path.join(path, "resources", "auto_document_metadata.pkl")  #
auto_iid_path = os.path.join(path, "resources", "auto_inverse_index.pkl")  #


#################################################################################

def loadAutoResourses():
    global dm_path
    global iid_path
    dm = dm_path
    iid = iid_path
    dm_path = auto_dm_path
    iid_path = auto_iid_path

    df =  loadDocumentMetadata()
    iid = loadInverseIndexedDoc()

    dm_path = dm
    iid_path = iid
    return(df,iid)
def loadInverseIndexedDoc():
    if not os.path.exists(iid_path):
        dm = loadDocumentMetadata()

        import dataPreprocessing as dp
        dp.create_inverse_index(dm)

    inverse_index = pd.read_pickle(iid_path)
    global iit
    iit = inverse_index

    return (inverse_index)


def loadDocumentMetadata():
    if not os.path.exists(dm_path):
        print(dm_path)
        print(
            "Seems like the metadata is not created\n Select the database to create metadata"
        )

        import tkinter
        from tkinter import filedialog
        root = tkinter.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(
            parent=root, title='Open file to preProcess')

        import dataPreprocessing as dp
        dp.preprocess_text_data(filename)
    document_metadata = pd.read_pickle(dm_path)
    global df
    df = document_metadata
    return (document_metadata)


def loadDocuments():
    documents = pd.read_excel(doc_path)
    return documents


def loadResources():
    return(loadDocumentMetadata(), loadInverseIndexedDoc(), loadDocuments())


'''
def AutomateDocCreation():
    import tkinter
    from tkinter import filedialog
    root = tkinter.Tk()
    root.withdraw()
    # filename = filedialog.askdirectory(
    #     parent=root, title='Open folder to extract')
'''
