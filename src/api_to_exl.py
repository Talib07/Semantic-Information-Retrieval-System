

import xplore


import json
#import pandas as pd
from pandas.io.json import json_normalize



def automate_metadata_creation_online(field, argument):
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

    def format_data(data):
        """
        Utility function to extract the required information from the JSON string
        """
        df = json_normalize(data["articles"])
        #df.dropna(subset=['keyword'], inplace=True)
        cols = ["index_terms.ieee_terms.terms", "index_terms.author_terms.terms"]
        # for col in cols:
        #     isnull = df[col].isnull()
        #     df.loc[isnull, col] = [[[]] * isnull.sum()]

        df["keyword"] = df[cols[0]] + df[cols[1]]
        df.dropna(subset=['keyword'], inplace=True)
        # Next, we convert the list of keywords to a string
        df["keyword"] = df["keyword"].apply(lambda x: ', '.join(map(str, x)))
        new_df = df[["title", "keyword", "abstract"]]
        new_df.dropna(subset = ['keyword'],inplace =True)
        new_df.to_excel("new.xlsx",index = False)
        #new_df["topic"] = topic
        
        return new_df

    query = xplore.xploreapi.XPLORE('b4yy7djd3gp54ckk3ywe7zhy')
    df1 = search_ieee(field, argument)
    df2 = format_data(df1)
    #print(df2.shape)
    #print(df2.head())
    



# change these parameters for different results
'''
Parameters:
            field - name of the data field being queried or the type of query;
            accepted values are: "abstract", "article_title", "author", "doi",
            "index_terms", "meta_data", "publication_title", "publication_year",
            "querytext", "thesaurus_terms"
            query_str - the value to query in that data field
            year - the year of publication
'''

field = "article_title"
query_str = "natural language processing"

automate_metadata_creation_online(field, query_str)
