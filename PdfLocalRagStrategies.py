# Run first requirements and 
#!ollama pull llama3
# !ollama pull nomic-embed-text
# install poppler id strategy is hi_res
# unstructered API can only process ONE pdf by one, vbut fast strategie can process an entire directory
# not using api. 


import os
from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.title import chunk_by_title
from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


from Utils import Utils
import json

utils = Utils()

DLAI_API_KEY = utils.get_dlai_api_key()
DLAI_API_URL = utils.get_dlai_url()

s = UnstructuredClient(
    api_key_auth=DLAI_API_KEY,
    server_url=DLAI_API_URL,
)

#  preprocess pdfs inside pdfs directory
def preprocess_pdfs(directory):
  elements = []
  for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith(".pdf"):
            req = shared.PartitionParameters(
                files=files,
                strategy='hi_res',
                pdf_infer_table_structure=True,
                languages=["esp"],
            )
            try:
                resp = s.general.partition(req)
                print (json.dumps(resp.elements[:3], indent=2))
            except SDKError as e:
                print(e)    
  return resp.elements[:3]


pdf_elements = preprocess_pdfs("pdfscc")

"""
# chunking
chunked_elements = chunk_by_title(pdf_elements)

documents = []
for element in chunked_elements:
    metadata = element.metadata.to_dict()
    documents.append(Document(page_content=element.text,
                              metadata=metadata))

print(documents)
"""
