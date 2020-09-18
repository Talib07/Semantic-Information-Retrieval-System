from xlutils.copy import copy
from xlrd import open_workbook
import os
import PyPDF2


path = os.getcwd()

dirpath = os.path.join(path, "resources")
#file_list = os.listdir(dirpath)

act_fl = []

def doit():

    dirpath = os.path.join(path, "resources", "new_papers")
    #new_dirpath = os.path.join(path, "resources", "new_work_papers")

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

                #continue
                #print(info_dict.keys())
                if '/Title' not in info_dict.keys() or info_dict['/Title'] == 'untitled' or len(info_dict['/Title']) == 0:
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
        act_fl.append(file)
    return(title_l, keywords_l)
    # if len(keywords)==0:

    #     continue

    # i += 1


doit()
print(len(act_fl))

import shutil
os.mkdir('new_work_papers')
for file in act_fl:
    shutil.copy(os.path.join(dirpath,"new_papers",file),'new_work_papers')

#rb = open_workbook(os.path.join(dirpath, "Dataset_100.xlsx"))
#print(rb.sheet_by_index(0).nrows)
# wb = copy(rb)

# nrows = 0
# ncols = 0
# for sheet in rb.sheets():
#     nrows = sheet.nrows
#     ncols = sheet.ncols
# #print(nrows, ncols)
# title, keywords = doit()
# # for i in range(len(title)):
# #     print(title[i])
# #     print("-",keywords[i],"\n")
# #     print(file_list[i])
# s = wb.get_sheet(0)

# for i in range(len(title)):
#     s.write(nrows, 0, title[i])
#     s.write(nrows, 1, keywords[i])
#     nrows+=1
# wb.save(os.path.join(dirpath, "update.xls"))
