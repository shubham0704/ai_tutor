
import sys
sys.path.insert(0, '../ai_tutor')
import spacy
# other dependecies
from ai_tutor import get_triples
from ai_tutor.get_triples import QuestionGenerator
from ai_tutor.svo_extractor import get_svo, preprocess
from ai_tutor.sentence_selector import SentenceSelection

nlp = spacy.load("en")

def extract_best_sents(filename, ratio=0.4):

	ss = SentenceSelection(ratio=ratio)
	sentences = ss.prepare_sentences(filename)
	sents = list(sentences.values())[:]
	return sents

def preprocessing(filename):
	
	sents = extract_best_sents(filename) 
	for sent in sents:
		sent, doc = preprocess(sent)




# test functions
def test_extract_sentences():

	filename = "test/test_files/babur.txt"
	sents = extract_best_sents(filename)
	assert len(sents) > 0

def test_preprocess():

	filename = "test/test_files/babur.txt"
	preprocessing(filename)