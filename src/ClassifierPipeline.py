__author__ = 'truba'
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC
from sklearn import metrics


class Classifier:
    def __init__(self, pipe=None, gs_params=None):
        # vlaho --> nikad None s ==, != i sl.
        if pipe is not None:
            self.text_clf = pipe
        else:
            self.text_clf = Pipeline([('vect', CountVectorizer()),
                                      ('tfidf', TfidfTransformer()),
                                      ('clf', MultinomialNB())
                                      ])
        if gs_params is not None:
            self.gs_params = gs_params
        else:
            self.gs_params = {'vect__ngram_range': [(1, 1), (1, 2)],
                              'tfidf__use_idf': (True, False),
                              'clf__alpha': (1e-2, 1e-3)
                              }

    def grid_search(self, documents, labels):
        gs_clf = GridSearchCV(self.text_clf, self.gs_params, n_jobs=-1, cv=5)
        gs_clf.fit(documents, labels)
        best_parameters, score, _ = max(gs_clf.grid_scores_, key=lambda x: x[1])
        print("Score: " + str(score))
        for param_name in sorted(self.gs_params.keys()):
            print("%s: %r" % (param_name, best_parameters[param_name]))
        return gs_clf

    def fit(self, documents, labels):
        self.text_clf.fit(documents, labels)

    def predict(self, documents):
        return self.text_clf.predict(documents)

    def classification_report(self, labels, documents, label_names=None):
        return metrics.classification_report(labels, self.predict(documents), target_names=label_names)