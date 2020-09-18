# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 16:58:57 2020

@author: Debs
"""

from pandas.io.json import json_normalize
import json
import xplore


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
    for col in cols:
        isnull = df[col].isnull()
        df.loc[isnull, col] = [ [[]] * isnull.sum() ]
    
    df["keywords"] = df[cols[0]] + df[cols[1]] 
    # Next, we convert the list of keywords to a string 
    df["keywords"] = df["keywords"].apply(lambda x: ', '.join(map(str, x))) 
    new_df = df[["title","keywords", "abstract"]]
    new_df["topic"] = topic
    return new_df


def run():
    #take input field and argument
    field = ""
    argument =""
    df1 = search_ieee(field,argument)
    topic =""
    df2 = format_data(df1, topic)
    

#API INITIALIZATION
query = xplore.xploreapi.XPLORE('b4yy7djd3gp54ckk3ywe7zhy')
df1 = search_ieee("article_title", "natural language processing")
print(format_data(df1,"topic").shape)
# ## Manual repeated calls
# # df1 = search_ieee("t1", "t2")
# # df2 = format_data(df1, "t4")

# # to append df2 at the end of init_df dataframe 
# # init_df.append(df2) 

# #FINAL WRITE
# # final_df.to_csv('data_repo.csv', index=False)
