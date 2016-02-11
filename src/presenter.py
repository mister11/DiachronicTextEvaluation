__author__ = 'truba'
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.grid_search import GridSearchCV
from sklearn.naive_bayes import MultinomialNB
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
from sklearn.externals import joblib

sizes = (2, 3)
tags = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'POS',
        'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT',
        'WP',
        'WP$', 'WRB']
model, jar = '../data/pos_tagger/english-bidirectional-distsim.tagger', '../data/pos_tagger/stanford-postagger.jar'
pickles = '../data/pickles/'




#return 1900
#gran F, M, C
def evaluate(granularity, text):

    preprocessor = Preprocessor()
    entry = TextEntry()
    entry.body = text
    preprocessor.entries = [entry]

    data = preprocessor.get_clean_data()
    ncharsAll = preprocessor.getNChars(items=data, freq=20)

    test_data_raw = preprocessor.get_clean_data()
    test_raw_text = preprocessor.get_raw_words()

    count_vect = joblib.load('../models/t1/vec_count.joblib')
    tfidf_transform = joblib.load('../models/t1/tfidf_transform.joblib')

    data_counts = count_vect.transform(test_data_raw)
    test_data = tfidf_transform.transform(data_counts)

    dense_test = test_data.toarray()

    vocab = count_vect.vocabulary_
    nchars = []
    for nchar in ncharsAll:
        if nchar not in vocab:
            nchars.append(nchar)

    numOfTags = len(tags)
    ncharVecSize = len(nchars)

    tag_vecs = []
    pos = POSTagger(model, jar, java_options='-mx2500m')
    for i, text in enumerate(test_raw_text):
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

    for i, text in enumerate(test_raw_text):
        if i % 100 == 0:
            print(i)
        words = text.split()
        ncharVec = np.zeros(ncharVecSize)
        for word in words:
            for size in sizes:
                text_nchars = [word[i:i + size] for i in range(len(word) - size + 1)]
                text_nchars_with_freq = Counter(text_nchars)
                for nchar, freq in text_nchars_with_freq.items():
                    if nchar in nchars:
                        ncharVec[nchars.index(nchar)] = freq / len(words)

        test_data[i] = np.concatenate((dense_test[i], ncharVec, tag_vecs[i]))

    svm_l = joblib.load('../models/t1/svm_l_'+granularity+'/svm_l_'+granularity+'.joblib')
    svm_u = joblib.load('../models/t1/svm_l_'+granularity+'/svm_l_'+granularity+'.joblib')

    evaluator = ClfEval(svm_l, svm_u)
    return evaluator.eval_data(csr_matrix(test_data))

evaluate("C",'What does it mean? At the end of Scene IV, a guard, Marcellus, says these famous words to Horatio. After Hamlet follows the ghost, Marcellus and Horatio know they have to follow as well, because Hamlet is acting so impulsively. Marcelluss words are remarking on how something evil and vile is afoot.')