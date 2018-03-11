# extract all triples and store them in npy format
# import sys, os
# sys.path.append(os.path.expanduser('~') + '/models/syntaxnet/')
from svo_extractor import get_svo, preprocess
from sentence_selector import SentenceSelection
import spacy
import re
nlp = spacy.load("en")
# def preprocess(sent):

# 	tok_sent = [word.lower() for word in sent.split()]
# 	return tok_sent


class QuestionGenerator:


	def get_text(self):
		pass

	def get_questions(self, sent):

		# given a sentence generate questions
		# return list of (question, answer)

		# Step1 take a sentence and triple so all those triples will act as fill in the blanks
		tok_sent, doc = preprocess(sent)
		triples = get_svo(doc)	
		# replace the token with a spl char like blank_0
		# fill in the blanks type questions
		questions = []

		for i, svo in enumerate(triples):
			for j, ele in enumerate(svo):
				question = tok_sent[:]
				for k, token in enumerate(tok_sent):
					if token == ele:
						question[k] = 'blank_0'
						answer = ele
						questions.append((question,answer))
						break
					elif re.search("[0-9]+", token):
						question[k] = 'blank_0'
						answer = token
						questions.append((question,answer))
						break

		return questions

	def generate_questions(self, sentences):
		questions = []
		for sent in sentences:
			questions.append(self.get_questions(sent))

		return questions


if __name__ == '__main__':

	document = 'sun.txt'
	qgen = QuestionGenerator()
	ratio = 0.4
	ss = SentenceSelection(ratio=ratio)
	sentences = ss.prepare_sentences(document)
	sents = sentences.values()[:]
	# for sent in sentences.values():
	# 	sents.append(sent)
	# print sents
	questions = qgen.generate_questions(sents)
	#print questions
	for question_set in questions:
		for question in question_set:
			print question,'\n'
