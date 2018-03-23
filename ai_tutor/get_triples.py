from __future__ import print_function
from ai_tutor.svo_extractor import get_svo, preprocess
from ai_tutor.sentence_selector import SentenceSelection
import spacy
import string
import re

nlp = spacy.load("en")


class QuestionGenerator:
    def get_text(self):
        pass

    def get_questions(self, sent):

        # given a sentence generate questions
        tok_sent, doc = preprocess(sent)
        # print (tok_sent, doc) 
        s, _, o = get_svo(doc)
        triples = (s, o)
        # fill in the blanks type questions
        questions = []
        # print ('subjects are - ',s, 'objects are -',o)

        for i, svo in enumerate(triples):
            for j, ele in enumerate(svo):
                question = tok_sent[:]
                for k, token in enumerate(tok_sent):
                    if token == ele:
                        question[k] = 'blank0'
                        answer = ele
                        questions.append((question, answer))
                        break

        return questions

    def generate_questions(self, sentences):
        questions = []
        for sent in sentences:
            questions.append(self.get_questions(sent))
        newquestions = []
        answers = []
        for question_set in questions:
            for question in question_set:
                temp = [word.replace('_', ' ') for word in question[0]]
                newquestions.append(' '.join(temp))
                answers.append(question[1].replace('_', ' '))
        return newquestions, answers