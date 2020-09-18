import io
import unicodedata
import pdfminer
import re
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

import os
path = os.getcwd()
dirpath = os.path.join(path, "MAJOR", "resources", "papers")

# Perform layout analysis for all text
laparams = pdfminer.layout.LAParams()
setattr(laparams, 'all_texts', True)


def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=laparams)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            break

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    if text:
        k = unicodedata.normalize('NFKD', text).encode('ascii', 'replace')
        k = k.decode('utf-8')
        # print(k[1000:2000])

        if re.search(r'\n\nKeywords:\n', k) is not None:
            startindex = re.search(r'\n\nKeywords:\n', k).end()
            k = k[startindex:]
            k = k[:500]
            endindex = re.search(r'\n\n[a-zA-Z]', k).start()
            keywords = k[:endindex]
            keywords = keywords.lower()

            keywords = re.sub("[?]", ' ', keywords)
            keywords = keywords.split('\n')
            keys = []
            for i in keywords:
                keys.append(i.replace("\n", " "))
            print(keys)
        elif re.search(r'Index Terms', k) is not None:
            startindex = re.search(r'Index Terms', k).end()
            k = k[startindex:]
            k = k[:500]
            endindex = re.search(r'\n\n[a-zA-Z]', k).start()
            keywords = k[:endindex]
            keywords = keywords.lower()

            keywords = re.sub("[\n?]", ' ', keywords)
            print(keywords)
            keywords = keywords.split(',')

            # for i in keywords:
            #     keys.append(i.replace("\n"," "))
            print(keywords)
        return ""

 
text = extract_text_from_pdf(os.path.join(
    dirpath, "07814696.pdf"))
print(text)

# import unicodedata
# import re
# import io
# from pdfminer.converter import TextConverter
# from pdfminer.pdfinterp import PDFPageInterpreter
# from pdfminer.pdfinterp import PDFResourceManager
# from pdfminer.pdfpage import PDFPage


# def extract_text_by_page(pdf_path):
#     with open(pdf_path, 'rb') as fh:
#         for page in PDFPage.get_pages(fh,
#                                       caching=True,
#                                       check_extractable=True):
#             resource_manager = PDFResourceManager()
#             fake_file_handle = io.StringIO()
#             converter = TextConverter(resource_manager, fake_file_handle)
#             page_interpreter = PDFPageInterpreter(resource_manager, converter)
#             page_interpreter.process_page(page)
#             text = fake_file_handle.getvalue()
#             yield text
#             # close open handles
#             converter.close()
#             fake_file_handle.close()


# def extract_text(pdf_path):
#     for page in extract_text_by_page(pdf_path):
#         k = unicodedata.normalize('NFKD', page).encode('ascii', 'replace')
#         print(k)
#         startindex = re.search(r'Keywords', k).end()


#         k = k[startindex:]
#         endindex = re.search(r'/', k).start()
#         keywords = k[:endindex]
#         keywords.lower()
#         re.sub("[ ,;']", ' ', keywords)
#         print(keywords)


# if __name__ == '__main__':
#     print(extract_text("1-s2.0-S0306437917301503-main.pdf"))


# # Get the outlines of the document.
# outlines = document.get_outlines()
# for (level, title, dest, a, se) in outlines:
#     print(level, title)

# from pdfminer.pdfinterp import PDFPageInterpreter
# from pdfminer.pdfinterp import PDFResourceManager
# from pdfminer.pdfpage import PDFPage
# from pdfminer.converter import TextConverter
# import io


# file = "1-s2.0-S0306437917301503-main.pdf"

# resource_manager = PDFResourceManager()
# fake_file_handle = io.StringIO()
# converter = TextConverter(resource_manager, fake_file_handle)
# fake_file_handle = io.StringIO()
# converter = TextConverter(resource_manager, fake_file_handle)
# page_interpreter = PDFPageInterpreter(resource_manager, converter)
# with open(file, 'rb') as f:
#     page_number = 0
#     for pageno, page in enumerate(PDFPage.get_pages(f)):
#         if page_number == pageno:
#             page_interpreter.process_page(page)
#             data = fake_file_handle.getvalue()
#     converter.close()
#     fake_file_handle.close()

#     if data:
#         print(data)
