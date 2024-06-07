# General notes: Run first requirements and  conda activate localrag
# !ollama pull llama3
# !ollama pull nomic-embed-text
# install poppler id strategy is hi_res
# unstructeredAPI can only process ONE pdf by one, but fast strategy can process an entire
# directory not using api.

# README: This file is used to convert pdf to jsonl in order to make datasets for trainning models
import os
import json
from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.title import chunk_by_title
from unstructured_client import UnstructuredClient
from langchain_core.documents import Document
from Utils import Utils


utils = Utils()
DLAI_API_KEY = utils.get_dlai_api_key()
DLAI_API_URL = utils.get_dlai_url()

s = UnstructuredClient(
    api_key_auth=DLAI_API_KEY,
    server_url=DLAI_API_URL,
)

#  preprocess pdfs inside pdfscc directory
def preprocess_pdfs(directory):
    elements = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf"):
                elems = partition_pdf(
                    filename=os.path.join(root,file),
                    include_page_breaks=True,
                    infer_table_structure=True,
                    languages=['esp'], 
                    strategy="fast")
                elements.extend(elems)
                
        return elements
    
pdf_elements = preprocess_pdfs("pdfscc")


# chunking
chunked_elements = chunk_by_title(pdf_elements)

documents = []
for element in chunked_elements:
    metadata = element.metadata.to_dict()
    documents.append(Document(page_content=element.text,
                              metadata=metadata))


# Convert documentos a JSON
def document_to_dict(document):
    return {
        "page_content": document.page_content,
        "metadata": document.metadata
    }

documents_json = json.dumps([document_to_dict(doc) for doc in documents], ensure_ascii=False)

# Convert documentos a JSONL y guardar en un archivo
def save_as_jsonl(documents, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for document in documents:
            json_line = json.dumps(document_to_dict(document), ensure_ascii=False)
            f.write(json_line + '\n')

# Llamada a la función para guardar los documentos
save_as_jsonl(documents, 'documents.jsonl')
