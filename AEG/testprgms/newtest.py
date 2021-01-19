
# # pip install tika
# import PyPDF2
# import parser
#
# strv="C:/Users/BOON/Downloads/mca3_pdfs.pdf"
# pdf_file = open(strv,'rb')
# read_pdf = PyPDF2.PdfFileReader(pdf_file)
# number_of_pages = read_pdf.getNumPages()
# page = read_pdf.getPage(0)
# page_content = page.extractText()
# # raw = parser.from_file(strv)
# # print(raw['content'])
# print(page_content.encode('utf-8'))
import pdfplumber as pdfplumber

with pdfplumber.open(r'C:/Users/BOON/Downloads/IRJET-V4I3718.pdf') as pdf:
    for page in pdf.pages:
        first_page = page
        print(page.extract_text())

# from pdfminer.converter import TextConverter
# from pdfminer.layout import LAParams
# from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# from pdfminer.pdfpage import PDFPage
#
# import StringIO
#
# rsrcmgr=PDFResourceManager()
# sio=StringIO()
# codec='utf-8'
# laparam=LAParams()
# device=TextConverter(rsrcmgr,sio,codec=codec,laparams=laparam)
# interpreter=PDFPageInterpreter(rsrcmgr,device)
# strv="C:/Users/BOON/Downloads/mca3_pdfs.pdf"
# fp=open(strv,'rb')
# for page in PDFPage.get_pages(fp):
#     interpreter.process_page(page)
# fp.close()
# del fp
# text=sio.getvalue()
# device.close()
# sio.close()
# del device
# del sio
# print(text)
#
