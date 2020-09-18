# dataPreprocessing.py
'''
To-do list
1. improve the lemmatization part


'''


from pandas.io.json import json_normalize
import xplore
import json
import pandas as pd
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag


########


# Revisit


##########
def preprocess_text_data(docpath):
    # lower-casing step
    def lowercase(data):
        data['title'] = data['title'].str.lower()
        data['keyword'] = data['keyword'].str.lower()
        data['abstract'] = data['abstract'].str.lower()
    # remove punctuation

    def remove_punctuation(data):
        data['title'] = data['title'].str.replace('[^\w\s]', ' ')
        data['keyword'] = data['keyword'].str.replace('[^\w\s]', ' ')
        data['abstract'] = data['abstract'].str.replace('[^\w\s]', ' ')
    # tokenization

    def tokens(data):
        df = pd.DataFrame()
        
        # cols = ['keyword']
        # for col in cols:
        #     isnull = data[col].isnull()
        #     data.loc[isnull, col] = [[[]] * isnull.sum()]
        

        df['title'] = data['title'].apply(word_tokenize)
        df['keyword'] = data['keyword'].apply(word_tokenize)
        df['abstract'] = data['abstract'].apply(word_tokenize)
        return df

    def get_wordnet_pos(word):
        """Map POS tag to first character lemmatize() accepts"""
        tag = pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}

        return tag_dict.get(tag, wordnet.NOUN)

    def lemmatize(new_data):
        lemmatizer = WordNetLemmatizer()
        l1 = []
        l2 = []
        l3 = []
        for item in new_data['title']:
            l1.append([lemmatizer.lemmatize(word, get_wordnet_pos(word))
                       for word in item])
        for item in new_data['abstract']:
            l3.append([lemmatizer.lemmatize(word, get_wordnet_pos(word))
                       for word in item])
        for item in new_data['keyword']:
            l2.append([lemmatizer.lemmatize(word, get_wordnet_pos(word))
                       for word in item])

        df = pd.DataFrame({'title': l1, 'keyword': l2, 'abstract': l3})
        return df

    ################################################################
    if type(docpath) == str:
        data = pd.read_excel(docpath)
    else:
        data = docpath
    lowercase(data)
    data.dropna(subset = ['keyword'],inplace =True)
    remove_punctuation(data)
    new_data = tokens(data)

    # Stop Word Removal
    stop = stopwords.words('english')
    new_data['title'] = new_data['title'].apply(
        lambda x: [item for item in x if item not in stop])
    new_data['keyword'] = new_data['keyword'].apply(
        lambda x: [item for item in x if item not in stop])
    new_data['abstract'] = new_data['abstract'].apply(
        lambda x: [item for item in x if item not in stop])

    # Lemmatization
    ###############################################################

    df = lemmatize(new_data)
    # Storing the dataframe locally using pickle
    # path = os.getcwd()  #
    # meta = os.path.join(path, "resources", "document_metadata.pkl")  #
    # metapath = meta.replace(os.sep, "/")
    # df.to_pickle(metapath)

    return(df)
#############################################################################################


def create_inverse_index(dataframe):
    inverse_index = {}
    m, n = dataframe.shape
    for i, row in dataframe.iterrows():
        cols = ['keyword','title']
        for col in cols:
            # coz 0-abstract, 1-keywords, 2-title
            for key in row[col]:
                if key in inverse_index:
                    inverse_index[key].add(i)
                else:
                    inverse_index[key] = set()
                    inverse_index[key].add(i)

    for key, value in inverse_index.items():
        l = []
        l.append(value)
        inverse_index[key] = l
    inverse_index_dataframe = pd.DataFrame.from_dict(inverse_index, orient='index')

    # path = os.getcwd()
    # indexpath = os.path.join(path, "resources", "inverse_index.pkl")  #
    # indexpath = indexpath.replace(os.sep, "/")
    # inverse_index_dataframe.to_pickle(indexpath)

    return (inverse_index_dataframe)


def create_metadata():
    import tkinter
    from tkinter import filedialog
    path = os.getcwd()  #
    meta = os.path.join(path, "resources", "document_metadata.pkl")  #
    metapath = meta.replace(os.sep, "/")
    indexpath = os.path.join(path, "resources", "inverse_index.pkl")  #
    indexpath = indexpath.replace(os.sep, "/")

    root = tkinter.Tk()
    root.withdraw()
    filename = filedialog.askopenfilename(
        parent=root, title='Open file to preProcess')
    dm = preprocess_text_data(filename)
    dm.to_pickle(metapath)
    iid = create_inverse_index(dm)
    iid.to_pickle(indexpath)
    return(dm, iid)


def updata_metadata(df2):
    import loader
    df = loader.loadDocumentMetadata()
    # print(df.shape)
    df2 = preprocess_text_data(df2)
    df = df.append(df2, ignore_index=True)
    print(df2.shape)
    # print(df.shape)
    iid = create_inverse_index(df)
    path = os.getcwd()  #
    meta = os.path.join(path, "resources", "document_metadata.pkl")  #
    metapath = meta.replace(os.sep, "/")
    indexpath = os.path.join(path, "resources", "inverse_index.pkl")  #
    indexpath = indexpath.replace(os.sep, "/")

    df.to_pickle(metapath)
    iid.to_pickle(indexpath)


def automate_metadata_creation_offline():
    # to be added
    # select a folder containing the documents
    import PyPDF2
    import tkinter
    from tkinter import filedialog

    from xlrd import open_workbook
    from xlutils.copy import copy
    datapath = os.path.join(os.getcwd(), "resources", "Dataset_100.xlsx")
    rb = open_workbook(datapath)
    wb = copy(rb)

    root = tkinter.Tk()
    root.withdraw()
    dirpath = filedialog.askdirectory(
        parent=root, title='Select folder containing the documents')
    file_list = os.listdir(dirpath)

    title_l = []
    keywords_l = []
    for file in file_list:
        with open(os.path.join(dirpath, file), 'rb') as fh:
            pdfFileObj = fh
            reader = PyPDF2.PdfFileReader(pdfFileObj)
            info = reader.getDocumentInfo()
            title = info.title
            info_dict = dict(info)
            # print(info_dict)
            # print(file)
            if '/Keywords' not in info_dict.keys():

                continue
                print(info_dict.keys())
                if info_dict['/Title'] == 'untitled' or len(info_dict['/Title']) == 0:
                    #print("This Thissssss")
                    continue
                else:
                    import preProcessing as pp
                    keywords = ', '.join(pp.getPreprocessedKeywords(str(info_dict['/Title'])))
            else:
                if len(info_dict['/Keywords']) == 0:
                    import preProcessing as pp
                    keywords = ', '.join(pp.getPreprocessedKeywords(str(info_dict['/Title'])))
                else:
                    keywords = str(info_dict['/Keywords']).replace(";", ',')

        keywords_l.append(keywords)
        title_l.append(title)

    nrows = rb.sheet_by_index(0).nrows
    s = wb.get_sheet(0)

    for i in range(len(title_l)):
        s.write(nrows, 0, title_l[i])
        s.write(nrows, 1, keywords_l[i])
        s.write(nrows, 2, "a")
        nrows += 1
    wb.save(os.path.join(os.getcwd(), "resources", "update.xls"))


def automate_metadata_creation_online(field, argument, topic):
    def search_ieee(field, query_str):
        """
        Function to use the IEEE Xplore API for customized search
        Parameters:
            field -  name of the data field being queried or the type of query;
            accepted values are: "abstract", "article_title", "author", "doi",
            "index_terms", "meta_data", "publication_title","publication_year",
            "querytext", "thesaurus_terms"
            query_str - the value to query in that data field
            year - the year of publication
        """
        query.searchField(field, query_str)
        query.dataType('json')
        query.dataFormat('raw')
        data = query.callAPI()
        parsed_json = json.loads(data.decode('utf-8'))
        return parsed_json

    def format_data(data, topic):
        """
        Utility function to extract the required information from the JSON string
        """
        df = json_normalize(data["articles"])
        cols = ["index_terms.ieee_terms.terms", "index_terms.author_terms.terms"]
        # for col in cols:
        #     isnull = df[col].isnull()
        #     df.loc[isnull, col] = [[[]] * isnull.sum()]
        df["keyword"] = df[cols[0]] + df[cols[1]]
        # Next, we convert the list of keywords to a string
        df["keyword"] = df["keyword"].apply(lambda x: ', '.join(map(str, x)))
        new_df = df[["title", "keyword", "abstract"]]
        new_df.dropna(subset=['keyword'], inplace=True)
        new_df.to_excel(os.join("resources","new.xlsx"), index=False)
        #new_df["topic"] = topic
        return new_df
    query = xplore.xploreapi.XPLORE('b4yy7djd3gp54ckk3ywe7zhy')

    # field = input("field:")
    # argument = input("argument:") # input
    # topic = input("topic:")  # input
    # field = "article_title"
    # argument ="machine learning"
    # topic ="topic"
    df1 = search_ieee(field, argument)
    df2 = format_data(df1, topic)
    # print(df2.shape)
    updata_metadata(df2)

    #import loader
    #init_df = loader.loadDocuments()
