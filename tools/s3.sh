#!/usr/bin/env bash
# export UNSTRUCTURED_API_KEY=

unstructured-ingest \
  s3 \
  --remote-url s3://datapp1234/pdfs/ \
  --anonymous \
  --strategy fast \
  --chunk-elements \
  --ocr-languages eng \
  --encoding utf8 \
  --output-dir s3-small-batch-output \
  --num-processes 9 \
  --partition-by-api \
  --api-key "$UNSTRUCTURED_API_KEY"

