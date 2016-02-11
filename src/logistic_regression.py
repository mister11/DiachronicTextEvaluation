__author__ = 'truba'

from sklearn.cross_validation import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from Preprocessor import Preprocessor
from ClassifierPipeline import Classifier
from Preprocessor import Preprocessor
from sklearn.linear_model import LogisticRegression
from Models import WordLabel

def find_classes(y_vector):
    resoults = []
    for y in y_vector:
        if y not in resoults:
            resoults.append(y)
    return resoults

def print_best_word_label_pairs(num_of_pairs, X, y):
    vectorizer = CountVectorizer()
    X_vec = vectorizer.fit_transform(X)
    transformer = TfidfTransformer()
    X_trans = transformer.fit_transform(X_vec)
    clf = LogisticRegression()
    clf.fit(X_trans, y)
    classes = find_classes(y)
    words = vectorizer.get_feature_names()
    list = []
    coefs = clf.coef_
    for class_index in range(coefs.shape[0]):
        for word_index in range(coefs.shape[1]):
            list.append(WordLabel(words[word_index], classes[class_index], coefs[class_index][word_index]))
    list.sort(key=lambda x: x.percentage, reverse=True)

    for i in range(num_of_pairs):
        pair = list[i]
        print(pair)



preprocessor = Preprocessor('../data/t2data/training08T2.txt', '../data/t1data/training08T1.txt')
data = preprocessor.get_clean_data()
labels_lower, labels_upper = preprocessor.labels_for_years(year_type="C")
Xl_train, Xl_test, yl_train, yl_test = train_test_split(data, labels_lower, test_size=0.3)

print_best_word_label_pairs(10, Xl_train, yl_train)

# print len(Xl_train)
# print len(Xl_train[0])
# print Xl_train[0]
#
# vectorizer = CountVectorizer()
# Xl_train = vectorizer.fit_transform(Xl_train)
#
#
# print len(vectorizer.get_feature_names())
#
# transformer = TfidfTransformer()
# Xl_train = transformer.fit_transform(Xl_train)
#
# print Xl_train.shape
#
# clf = LogisticRegression()
# clf.fit(Xl_train, yl_train)
#
# print Xl_train.shape
# print len(yl_train)
# print clf.coef_.shape
# print sum(clf.coef_[0])
# print sum(clf.coef_.T[0])