__author__ = 'truba'


from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

def multinomial_pipe():
    return Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB())
                     ])


def multinomial_gs_params():
    return {'vect__ngram_range': [(1, 1), (1, 2), (1, 3)],
            'clf__alpha': [x for x in range(1, 10, 1)]
            }

def logistic_regression_pipe():
    return Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', LogisticRegression())
                     ])

def logistic_regression_params():
     return {'vect__ngram_range': [(1, 1)],
            'clf__C': [2 ** x for x in range(-5, 5, 1)]
            }

def linear_svm_pipe():
    return Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', SVC(kernel='linear'))
                     ])


def linear_svm_gs_params():
    return {'vect__ngram_range': [(1, 1), (1, 2), (1, 3)],
            'clf__C': [2 ** x for x in range(-5, 5, 1)]
            }


def rbf_svm_pipe():
    return Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', SVC(kernel='rbf'))
                     ])


def rbf_svm_gs_params():
    return {'vect__ngram_range': [(1, 1), (1, 2), (1, 3)],
            'clf__C': [2 ** x for x in range(1, 6, 1)],
            'clf__gamma': [2 ** x for x in range(-9, -3, 1)]
            }


def dt_pipe():
    return Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', DecisionTreeClassifier())
                     ])


def dt_gs_params():
    return {'vect__ngram_range': [(1, 1), (1, 2), (1, 3)],
            'clf__min_samples_split': [x for x in range(2, 20, 1)]
            }
