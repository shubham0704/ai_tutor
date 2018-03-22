#! /bin/bash
pip install spacy
pip install nltk
apt-get install swig
apt-get install libpulse-dev
python -m spacy download en
python -m nltk.downloader stopwords
pip install textract