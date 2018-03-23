from __future__ import print_function
from ai_tutor.svo_extractor import get_svo, preprocess
from ai_tutor.sentence_selector import SentenceSelection
from ai_tutor.match import best_match, prepro

# other dependencies
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
import networkx as nx
import spacy
import re
import operator
import json

nlp = spacy.load("en")


class GraphBuilder:
    unique_dict = {}
    nid = 0
    unique_words = {}
    giant_graph = nx.DiGraph()

    def __init__(self, mc):
        self.mc = mc
        self.giant_graph.add_node(self.nid, label=self.mc)
        self.unique_dict[self.mc] = self.nid
        self.unique_words[self.nid] = self.mc
        self.nid += 1

    def gen_graph(self, triples, threshold=60):

        # check if length of the each triple is >0
        cnt = 0
        # case 1 : I do not have a subject
        # assign subject as self.mc

        for ele in triples:
            if len(ele) > 0:
                continue
            else:
                # print triples
                cnt += 1
        if cnt > 1:
            print("returning bro")
            return None

        if len(triples[0]) < 1:
            triples[0].append(self.mc)

        graph = nx.DiGraph()
        joined_triple = []
        for ele in triples:
            joined = " ".join(word for word in ele)
            joined_triple.append(joined)

        src_id = -1
        dest_id = -1
        # print (joined_triple)
        subject = joined_triple[0]
        # first calculate how much do the subjects match
        if subject != '':
        	#print("The main concept is given as: ", self.mc)
        	t = best_match(subject, self.mc)
	        if t >= 95:
	            # if i have some object ill join it using an edge to the mc
	            obj = joined_triple[2]
	            if obj:
	                if obj not in self.unique_dict:
	                    self.unique_dict[obj] = self.nid
	                    self.unique_words[self.nid] = obj
	                    self.giant_graph.add_node(self.nid, label=obj)
	                    self.giant_graph.add_edge(
	                        0,
	                        self.nid,
	                        key="parse_{}_{}".format(self.nid, 0), label=joined_triple[1])
	                    self.nid += 1
	        elif subject:
	            # option 1 just concatenate with graph
	            # option 2 just add the node with the graph
	            # I choose option2
	            if subject not in self.unique_dict:
	                self.unique_dict[subject] = self.nid
	                self.unique_words[self.nid] = subject
	                self.giant_graph.add_node(self.nid, label=subject)
	                self.giant_graph.add_edge(
	                    0,
	                    self.nid,
	                    key="parse_{}_{}".format(self.nid, 0))
	                self.nid += 1
	            obj = joined_triple[2]
	            if obj not in self.unique_dict and obj != '':
	                self.unique_dict[obj] = self.nid
	                self.unique_words[self.nid] = obj
	                self.giant_graph.add_node(self.nid, label=obj)
	                subj_id = self.unique_dict[subject]
	                self.giant_graph.add_edge(
	                    subj_id,
	                    self.nid,
	                    key="parse_{}_{}".format(self.nid, subj_id), label=joined_triple[1])
	                self.nid += 1

    def get_graph(self, sent):
        sent, doc = preprocess(sent)
        triples = get_svo(doc)
        # print triples
        return self.gen_graph(triples)

    def gen_giant_graph(self, sents):


        for sent in sents:
            self.get_graph(sent)
        # select which 2 graphs to concatenate at a time
        return self.giant_graph

    def plot_graph(self, graph):
        pos = nx.spring_layout(graph)
        label_dict = {}
        for node in graph.nodes():
            label_dict[node] = self.unique_words[node]

        nx.draw(graph, labels=label_dict, with_labels=True)
        plt.show()

    def get_json(self):
        data = json_graph.tree_data(self.giant_graph, root=0)
        return data


def main_concept(sents):
    svos = []
    for sent in sents:
        _, doc = preprocess(sent)
        svos.append(get_svo(doc))
    #print (svos)
    subjects = [svo[0] for svo in svos]
    # subjects = svos[:][0]

    # find the most prominent subject
    # step 1: find individual token frequencies
    freq_dict = {}
    for subj in subjects:
        subj = " ".join(ele for ele in subj)
        #subj = prepro(subj)
        if subj:
            tok_subj = subj.split()
            for tok in tok_subj:
                if tok in freq_dict:
                    freq_dict[tok] += 1
                else:
                    freq_dict[tok] = 1

    freqs = freq_dict.items()
    #print(freqs)
    freqs = sorted(freqs, key=operator.itemgetter(1), reverse=True)

    #print(freqs)
    return freqs[0][0]


def get_mind_map(document):
    ratio = 0.8
    ss = SentenceSelection(ratio=ratio)
    sentences = ss.prepare_sentences(document)
    sents = list(sentences.values())[:]

    mc = main_concept(sents)
    G = GraphBuilder(mc=mc)
    giant_graph = G.gen_giant_graph(sents)
    js = G.get_json()
    js = json.dumps(js)
    print(js)
    #G.plot_graph(giant_graph)
    # with open('babur.json', 'w+') as f:
    #     f.write(js)
    # print("done")


if __name__ == '__main__':
    document = 'babur.txt'
    # qgen = QuestionGenerator()
    ratio = 0.8
    ss = SentenceSelection(ratio=ratio)
    sentences = ss.prepare_sentences(document)
    sents = sentences.values()[:]

    mc = main_concept(sents)
    G = GraphBuilder(mc=mc)
    giant_graph = G.gen_giant_graph(sents)
    js = G.get_json()
    js = json.dumps(js)
    with open('babur.json', 'w+') as f:
        f.write(js)
    print("done")

    # print giant_graph.nodes()
    # print giant_graph.edges()
    # print(str(G.get_json()))
    G.plot_graph(giant_graph)
# print sents
