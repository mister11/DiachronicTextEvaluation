# Created by svenko11 on 5/18/15 9:24 PM
__author__ = 'Sven Vidak'

from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV
import PypeParams
from Preprocessor import Preprocessor
from ClassifierPipeline import Classifier
from Preprocessor import Preprocessor
from TimelineClassifier import TimelineClassifier
import ShifterParser
from ShifterParser import Shifter, ShifterDelegate
from Models import TextEntry
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import numpy as np
from scipy.sparse import csr_matrix
from collections import Counter
from main import ClfEval
from nltk.tag.stanford import POSTagger
import pickle
import os.path
import nltk


tags = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'POS',
		'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT',
		'WP',
		'WP$', 'WRB']

model, jar = '../data/pos_tagger/english-bidirectional-distsim.tagger', '../data/pos_tagger/stanford-postagger.jar'
pickles = '../data/pickles/'

preprocessor = Preprocessor('../data/t2data/moreT2.txt', '../data/t2data/training08T2.txt',
							'../data/t2data/trialT2.txt')
text_for_tags = preprocessor.get_raw_words()

numOfTags = len(tags)

file = pickles + 'train_tag_vecs_task2'
pos = POSTagger(model, jar, java_options='-mx2500m')

print(len(text_for_tags))
tag_vecs = []

for i, text in enumerate(text_for_tags):
	if i % 10 == 0:
		print(i)
	words = text.split()
	tag_vector = np.zeros(numOfTags)
	words_with_tags = pos.tag(words)
	only_tags = [tag for word, tag in words_with_tags[0]]
	tags_with_freq = Counter(only_tags)
	for tag, freq in tags_with_freq.items():
		tag_vector[tags.index(tag)] = freq / len(words)
	tag_vecs.append(tag_vector)

pickle.dump(np.array(tag_vecs), open(file, mode='wb'))