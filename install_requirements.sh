#! /bin/bash
pip install spacy
pip install nltk
pip install unidecode
pip install fuzzywuzzy
pip install networkx
pip install matplotlib
python -m spacy download en
python -m nltk.downloader stopwords
python -m nltk.downloader punkt
pip install textract