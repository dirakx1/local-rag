# Converts json files after processing them with unstructured api connected to an 
# s3 bucket
# Usage: python3.10 Json2Jsonl.py

import json
import os

def save_2_jsonl(input_directory, output_filename):
    documents = []
    
    # Recorrer todos los archivos en el directorio de entrada y cargar solo el campo "text"
    for root, _, files in os.walk(input_directory):
        for file in files:
            if file.endswith(".json"):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data:
                        if "text" in item:
                            documents.append({"text": item["text"]})
    
    # Guardar los documentos en un archivo JSONL
    with open(output_filename, 'w', encoding='utf-8') as f:
        for document in documents:
            json_line = json.dumps(document, ensure_ascii=False)
            f.write(json_line + '\n')

# Llamada a la función para guardar los documentos
save_2_jsonl('s3-small-batch-output', 'output.jsonl')
