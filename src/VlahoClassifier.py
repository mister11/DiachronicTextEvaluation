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

if __name__ == '__main__':
    # preprocessor = Preprocessor('../data/t2data/moreT2.txt', '../data/t2data/training08T2.txt',
    #                             '../data/t2data/trialT2.txt')
    preprocessor = Preprocessor('../data/t1data/moreT1.txt', '../data/t1data/training08T1.txt',
    '../data/t1data/trialT1.txt')

    data = preprocessor.get_clean_data()
    # year type is C, F or M
    labels_lower, labels_upper = preprocessor.labels_for_years_norm(year_type="C")

    ncharsAll = preprocessor.getNChars(items=data, freq=20)

    text_for_tags = preprocessor.get_raw_words()

    count_vect = CountVectorizer()
    data_counts = count_vect.fit_transform(data)
    joblib.dump(count_vect, '../models/t1/vec_count.joblib')

    tfidf_transform = TfidfTransformer()
    data_tfidf = tfidf_transform.fit_transform(data_counts)
    joblib.dump(tfidf_transform, '../models/t1/tfidf_transform.joblib')

    dense_tfidf = data_tfidf.toarray()

    # remove words in nchars that are already in vocabulary
    vocab = count_vect.vocabulary_
    nchars = []
    for nchar in ncharsAll:
        if nchar not in vocab:
            nchars.append(nchar)

    ncharVecSize = len(nchars)
    numOfTags = len(tags)
    newDataArray = np.empty((dense_tfidf.shape[0], dense_tfidf.shape[1] + ncharVecSize + numOfTags))
    print(len(nchars))
    print(len(data))
    print(len(tags))
    print(len(vocab))

    pos = POSTagger(model, jar, java_options='-mx2500m')

    tag_vecs = []

    file = pickles + 'train_tag_vecs_task1'
    tag_vecs = pickle.load(open(file, mode='rb'))

    for i, text in enumerate(text_for_tags):
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

        newDataArray[i] = np.concatenate((dense_tfidf[i], ncharVec, tag_vecs[i]))

    C = [2 ** i for i in range(-20, 20, 1)]
    # gamma = [2 ** i for i in range(-10, 10, 1)]
    params = {'C': C}

    svm_l = SVC(kernel='linear')

    svm_l = GridSearchCV(svm_l, params, n_jobs=-1, cv=5, verbose=3)
    # svm_l.fit(csr_matrix(newDataArray), labels_lower)
    # print(gs.best_params_)
    # exit()


    svm_l.fit(csr_matrix(newDataArray), labels_lower)

    svm_u = GridSearchCV(SVC(kernel='linear'), params, n_jobs=-1, cv=5, verbose=3)
    svm_u.fit(csr_matrix(newDataArray), labels_upper)

    joblib.dump(svm_l, '../models/t1/svm_l_C/svm_l_C.joblib')
    joblib.dump(svm_u, '../models/t1/svm_u_C/svm_u_C.joblib')

    preprocessor = Preprocessor('../data/evaluationScriptData/input/goldT2.txt')
    test_data_raw = preprocessor.get_clean_data()

    test_raw_text = preprocessor.get_raw_words()

    data_counts = count_vect.transform(test_data_raw)
    test_data = tfidf_transform.transform(data_counts)

    dense_test = test_data.toarray()

    ncharVecSize = len(nchars)
    test_data = np.empty((dense_tfidf.shape[0], dense_tfidf.shape[1] + ncharVecSize + numOfTags))

    pos = POSTagger(model, jar, java_options='-mx2500m')

    tag_vecs = []

    file = pickles + 'train_tag_vecs_taks1'
    tag_vecs = pickle.load(open(file, mode='rb'))

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

    shifer_lin_m = Shifter(ShifterParser.TYPE_TEXT_F, ClfEval(svm_l, svm_u), test_data=csr_matrix(test_data))

    shifer_lin_m.perform("../data/evaluationScriptData/input/goldT2.txt",
                         "../data/evaluationScriptData/med_sven_mnb_F.txt")

