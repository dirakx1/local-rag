# Run first requirements and 
# install poppler id strategy is hi_res

import os
from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.title import chunk_by_title
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from unstructured_client import UnstructuredClient


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

from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError
from unstructured.staging.base import dict_to_elements

path_to_pdf="pdfscc/Auto_SRVR-005-Caso-003_17-julio-2018.pdf"

with open(path_to_pdf, "rb") as f:
  files=shared.Files(
      content=f.read(),
      file_name=path_to_pdf,
      )
  req = shared.PartitionParameters(
    files=files,
    strategy="hi_res",
    hi_res_model_name="yolox",
    pdf_infer_table_structure=True,
    languages=['esp'],
    
  )
  try:
    resp = s.general.partition(req)
    elements = dict_to_elements(resp.elements)
    print (json.dumps(resp.elements[:], indent=4))
  except SDKError as e:
    print(e)




