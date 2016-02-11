__author__ = 'truba'

from sklearn.cross_validation import train_test_split
import PypeParams
from Preprocessor import Preprocessor
from ClassifierPipeline import Classifier
from Preprocessor import Preprocessor
from TimelineClassifier import TimelineClassifier
import ShifterParser
from ShifterParser import Shifter, ShifterDelegate
from Models import TextEntry


def multinomial_bayes(X_train, X_test, y_train, y_test):
    print("MULTINOMIAL BAYES")
    clf = Classifier(pipe=PypeParams.multinomial_pipe(), gs_params=PypeParams.multinomial_gs_params())
    clf.fit(X_train, y_train)
    clf.text_clf = clf.grid_search(X_train, y_train)
    print(clf.classification_report(y_test, X_test))
    print("\n\n\n")
    return clf.predict(X_test)


def linear_svm(X_train, X_test, y_train, y_test):
    print("LINEAR SVM")
    clf = Classifier(pipe=PypeParams.linear_svm_pipe(), gs_params=PypeParams.linear_svm_gs_params())
    clf.text_clf = clf.grid_search(X_train, y_train)
    return clf.text_clf


# print(clf.classification_report(y_test, X_test))
# print("\n\n\n")
# return clf.predict(X_test)


def rbf_svm(X_train, X_test, y_train, y_test):
    print("RBF SVM")
    clf = Classifier(pipe=PypeParams.rbf_svm_pipe(), gs_params=PypeParams.rbf_svm_gs_params())
    clf.text_clf = clf.grid_search(X_train, y_train)
    return clf.text_clf


# print(clf.classification_report(y_test, X_test))
# print("\n\n\n")
# return clf.predict(X_test)


def decision_three(X_train, X_test, y_train, y_test):
    print("DECISION THREE")
    clf = Classifier(pipe=PypeParams.dt_pipe(), gs_params=PypeParams.dt_gs_params())
    clf.text_clf = clf.grid_search(X_train, y_train)
    print(clf.classification_report(y_test, X_test))
    print("\n\n\n")
    return clf.predict(X_test)


class ClfEval():
    def __init__(self, clf, clf2=None):
        self.clf = clf
        self.clf2 = clf2

    def eval_data(self, data):
        predict = self.clf.predict(data)
        if self.clf2 is not None:
            predict2 = self.clf2.predict(data)
            return (predict + predict2) / 2
        return predict

    def evaluate_text(self, text):
        pre = Preprocessor()
        entry = TextEntry()
        entry.body = text
        pre.entries = [entry]
        predict = self.clf.predict(pre.get_clean_data())
        if self.clf2 is not None:
            predict2 = self.clf2.predict(pre.get_clean_data())
            return (predict + predict2) / 2
        return predict


if __name__ == '__main__':
    preprocessor = Preprocessor('../data/t1data/moreT1.txt', '../data/t1data/training08T1.txt',
                                '../data/t1data/trialT1.txt')
    data = preprocessor.get_clean_data()
    # year type is C, F or M
    labels_lower, labels_upper = preprocessor.labels_for_years_norm(year_type="F")

    Xl_train, Xl_test, yl_train, yl_test = train_test_split(data, labels_lower, test_size=0.3)


    # pred1l = multinomial_bayes(Xl_train, Xl_test, yl_train, yl_test)
    pred2l = linear_svm(Xl_train, Xl_test, yl_train, yl_test)
    pred3l = rbf_svm(Xl_train, Xl_test, yl_train, yl_test)
    # pred4l = decision_three(Xl_train, Xl_test, yl_train, yl_test)

    Xu_train, Xu_test, yu_train, yu_test = train_test_split(data, labels_upper, test_size=0.3)

    # pred1u = multinomial_bayes(Xu_train, Xu_test, yu_train, yu_test)
    pred2u = linear_svm(Xu_train, Xu_test, yu_train, yu_test)
    pred3u = rbf_svm(Xu_train, Xu_test, yu_train, yu_test)
    # pred4u = decision_three(Xu_train, Xu_test, yu_train, yu_test)

    shifer_lin_l = Shifter(ShifterParser.TYPE_TEXT_F, ClfEval(pred2l))
    shifer_rbf_l = Shifter(ShifterParser.TYPE_TEXT_F, ClfEval(pred3l))
    shifer_lin_u = Shifter(ShifterParser.TYPE_TEXT_F, ClfEval(pred2u))
    shifer_rbf_u = Shifter(ShifterParser.TYPE_TEXT_F, ClfEval(pred3u))

    shifer_lin_m = Shifter(ShifterParser.TYPE_TEXT_F, ClfEval(pred2l, pred2u))
    shifer_rbf_m = Shifter(ShifterParser.TYPE_TEXT_F, ClfEval(pred3l, pred3u))

    shifer_lin_l.perform("../data/evaluationScriptData/input/goldT1.txt",
                         "../data/evaluationScriptData/lower/lin_l_f.txt")
    shifer_rbf_l.perform("../data/evaluationScriptData/input/goldT1.txt",
                         "../data/evaluationScriptData/lower/rbf_l_f.txt")
    shifer_lin_u.perform("../data/evaluationScriptData/input/goldT1.txt",
                         "../data/evaluationScriptData/upper/lin_u_f.txt")
    shifer_rbf_u.perform("../data/evaluationScriptData/input/goldT1.txt",
                         "../data/evaluationScriptData/upper/rbf_u_f.txt")
    shifer_lin_m.perform("../data/evaluationScriptData/input/goldT1.txt",
                         "../data/evaluationScriptData/upper/lin_m_f.txt")
    shifer_rbf_m.perform("../data/evaluationScriptData/input/goldT1.txt",
                         "../data/evaluationScriptData/upper/rbf_m_f.txt")