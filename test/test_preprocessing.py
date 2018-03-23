
import sys
sys.path.insert(0, '../ai_tutor')
import spacy
import logging
# other dependecies
from ai_tutor.mind_map import main_concept, get_mind_map, GraphBuilder
from ai_tutor.get_triples import QuestionGenerator
from ai_tutor.svo_extractor import get_svo, preprocess
from ai_tutor.sentence_selector import SentenceSelection

nlp = spacy.load("en")
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('log')


def extract_best_sents(filename, ratio=0.2):

	ss = SentenceSelection(ratio=ratio)
	sentences = ss.prepare_sentences(filename)
	sents = list(sentences.values())[:]
	return sents

def preprocessing(filename):
	
	sents = extract_best_sents(filename) 
	for sent in sents:
		sent, doc = preprocess(sent)

def question_generator(filename):

	sents = extract_best_sents(filename)
	qgen = QuestionGenerator()
	for sent in sents:
		questions = qgen.generate_questions(sent)
		logging.info(questions)

def get_main_concept(filename):
	sents = extract_best_sents(filename)
	mc = main_concept(sents)
	return mc

def get_mind_map(filename):

    sents = extract_best_sents(filename)
    mc = get_main_concept(filename)
    G = GraphBuilder(mc=mc)
    giant_graph = G.gen_giant_graph(sents)

#test functions
def test_extract_sentences():

	filename = "test/test_files/babur.txt"
	sents = extract_best_sents(filename)
	assert len(sents) > 0

def test_preprocess():

	filename = "test/test_files/babur.txt"
	preprocessing(filename)

def test_question_generator():
	
	filename = "test/test_files/babur.txt"
	question_generator(filename)


def test_main_concept():

	filename = "test/test_files/babur.txt"	
	mc = get_main_concept(filename)
	assert mc is not None

def test_mind_map():

	filename = "test/test_files/babur.txt"	
	get_mind_map(filename)
