#!/bin/bash

mkdir deps && \
cd deps && \
# source venv/bin/activate && \
git clone https://github.com/ppke-nlpg/emmorphpy.git && \
cd emmorphpy && \
pip install -r requirements.txt && \
# Hungarian language model can ve modified - check: https://github.com/oroszgy/spacy-hungarian-models
pip install https://github.com/oroszgy/spacy-hungarian-models/releases/download/hu_core_ud_lg-0.3.1/hu_core_ud_lg-0.3.1-py3-none-any.whl && \
# German model Spacy LG installation
python -m spacy download de_core_news_lg