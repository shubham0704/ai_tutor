# import sys, os
# sys.path.append(os.path.expanduser('~') + '/models/syntaxnet/')
# import tree_gen
from __future__ import print_function
import spacy
import string
from nltk import Tree
# use spacy to ner and fill in the blank types
def to_nltk_tree(node):
	if node.n_lefts + node.n_rights > 0:
		return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
	else:
		return node.orth_


# def get_svo(text):
#   #subs = objs = verbs = None
#   subs = []
#   verbs = []
#   objs = []
#   parse_tree = tree_gen.get_tree(text)
#   print parse_tree
#   for token in parse_tree.token:
#     '''
#     if token.label == 'nsubj':
#       subs = token.word
#     elif token.label == 'root':
#       verbs = token.word
#     elif token.label == 'obj':
#       obj = token.word
#     else:
#       pass
#     '''

#     if "subj" in token.label:
#       subs.append(token.word)
#     elif token.label in ["root", "ex", "md"] or token.label.startswith("v"):
#       verbs.append(token.word)
#     elif "obj" in token.label or token.label.startswith("ob") or token.label=="nummod":
#       objs.append(token.word)


#   return (subs, verbs, objs)
nlp = spacy.load("en")

def get_svo(doc):

	subs = []
	verbs = []
	objs = []
	for tok in doc:
	#print('toks in doc are', tok, tok.tag_)
		if len(tok) < 3:
		    continue
		if tok.dep_ == "nsubj" or tok.tag_ == "WD":
		    subs.append(str(tok))
		elif tok.tag_.startswith("NN") and len(tok.tag_) > 2:
		    subs.append(str(tok))
		elif tok.tag_ == ["VBG", "VBD", "VBG"] or tok.dep_ == "ROOT":
		    verbs.append(str(tok))
		elif tok.dep_ in ["iobj", "dobj", "pobj"] or tok.tag_ == 'CD':
		    objs.append(str(tok))

	return (list(set(subs)), list(set(verbs)), list(set(objs)))


def ngram_join(sent, nchunks):
	for chunk in nchunks:
		chunk = str(chunk)
		#print chunk
		chunk_tok = chunk.split()

		ng_join = "_".join(e for e in chunk_tok)
		# replace the entity in the string with ng_join
		sent = string.replace(sent, chunk, ng_join)
	return sent

def chain_capitalize(sent):
	tok_sent = [tok for tok in sent.split()]
	temp = []
	new_tok_sent = []
	flag = 0
	n = len(tok_sent)
	for i, tok in enumerate(tok_sent):
		
		if flag == 1:
		    flag = 0
		    continue
		if len(str(tok)) > 1:
		    if tok[0].isupper() and tok[1].islower() or str(tok)=="of":
			    temp.append(tok)
			    if str(tok) == "of" and i+1<n:
			        flag = 1
			        temp.append(tok_sent[i+1])


		else:
			if len(temp) > 0:
				new_tok = '_'.join(tok for tok in temp)
				new_tok_sent.append(new_tok)
				temp = []
				new_tok_sent.append(tok)

  # new_tok_sent = list(set(new_tok_sent))
  # return new_tok_sent
  # for tok in tok_sent:
	return ' '.join(tok for tok in new_tok_sent)




def preprocess(sent):
	trans = string.maketrans(string.punctuation," "*len(string.punctuation))
	sent = sent.translate(trans)
	sent = chain_capitalize(sent)
	#print ('chained sentence is', sent)
	doc = nlp(sent.decode('utf-8'))
	# print [(tok.text, tok.label_) for tok in doc.ents]
	ncs = list(doc.noun_chunks)
	#print ('noun_chunks are', list(doc.noun_chunks))
	true_ncs = []
	for nc in ncs:
		nc_toks = str(nc).split(' ')
		#print ('nc toks are', nc_toks)
		num_toks = []
		other_toks = []
		for tok in nc_toks:
			try:
				if int(tok):
				#print ('numtok is', tok)
					num_toks.append(tok)
			# remove the numtok from tok add tok to true_ncs
			except:
			#print ('other tok is', tok)
				other_toks.append(tok)
		true_nc = ' '.join(other_toks)
		#print ('true nc is', true_nc)
		true_ncs.extend(num_toks)
		true_ncs.append(true_nc)
	ncs = true_ncs
	#print ('noun_chunks are', ncs)


	sent = ngram_join(sent, ncs)
	#print sent
	#print 'the noun chunks are', list(doc.noun_chunk4s)
	return [word.decode('utf-8') for word in sent.split()], nlp(sent.decode('utf-8'))

if __name__ == '__main__':
  sent = "Babur defeated Ibrahim Hussain Lodi at the First Battle of Panipat in 1526 CE and founded the Mughal empire"
  #sent = "The Sun is the star at the center of the Solar System"
  nlp = spacy.load("en")
  # doc = nlp(sent.decode())
  # #print 'noun_chunks', list(doc.noun_chunks)
  # sent = ngram_join(sent, list(doc.ents))
  # #print sent
  # doc = nlp(sent.decode())
  # sent , doc = preprocess(sent)
  # print [(tok, tok.dep_, tok.tag_) for tok in doc]

  #[to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]
  # sent = chain_capitalize(sent)
  sent , doc = preprocess(sent)
  #print [(tok, tok.dep_, tok.tag_) for tok in doc]
  #[to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]

  # print sent
  print (sent, doc)
  alls = get_svo(doc)
  print (alls)
  # print sent
