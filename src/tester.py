# Created by mister11 on 4/2/15 1:11 AM
__author__ = 'Sven Vidak'
from sklearn.datasets import fetch_20newsgroups
from sklearn.cross_validation import train_test_split

import Parser
from Preprocessor import Preprocessor
from ClassifierPipeline import Classifier

def test_parser():
    entries = Parser.parse('../data/training08T1.txt')
    print(entries[:10])

def test_preprocessor():
    preprocessor = Preprocessor('../data/training08T1.txt')
    print(preprocessor.get_clean_data()[:10])

def test_cassifier():
    #cls.fit(["djad jlk ajsd kjl", "sd jka sdks jdl", "dads ada sdasd as"], [1992,1992,1991]) - this is OK
    categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']
    twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)
    cls = Classifier()
    X_train, X_test, y_train, y_test = train_test_split(twenty_train.data[:100], twenty_train.target[:100], test_size=0.3, random_state=0)
    cls.text_clf = cls.grid_search(X_train, y_train)
    print(cls.clasification_repourt(y_test, X_test))

if __name__ == '__main__':
    #test_parser()
    test_preprocessor()
    #test_cassifier()