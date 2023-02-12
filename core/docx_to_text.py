from docx import Document

def docx_to_text(file_name):
    document = Document(file_name)
    text =''
    for para in document.paragraphs:
        text+="\n"+para.text
    return text
#print(str(text))
