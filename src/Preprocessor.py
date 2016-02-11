# Created by mister11 on 4/3/15 12:19 AM
__author__ = 'Sven Vidak'

from Models import TextPeriod, TextEntry
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import Parser
import re
import numpy as np

LOWER = 0
UPPER = 1

# todo - if needed (multiple calls on different places) its possible...
# todo -       ...to save all methods outputs in class variables so they are calculated only once

class Preprocessor():
    def __init__(self, *filenames):
        self.entries = Parser.parse(*filenames)
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.nchars = {}
        self.docsLength = np.empty(len(self.entries))

        self.min_lower_year = None
        self.min_upper_year = None
        self.max_lower_year = None
        self.max_upper_year = None

    # used in data analyzer
    def clean_entries(self):
        for entry in self.entries:
            entry_only_words = self.__extract_only_words(entry.body)
            words = entry_only_words.lower().split()
            # if word is not in stopwords, stemm it and save it
            cleaned = [self.stemmer.stem(word) for word in words if word not in self.stop_words]
            # create string from words that passed exam above (words that are not stopwords)
            entry.body = " ".join(cleaned)

    # used in main funcs
    def get_clean_data(self):
        entries_text = [entry.body for entry in self.entries]

        # "deletes" everything that is not a word or number (?, !, '...)
        entries_only_words = [self.__extract_only_words(entry_text) for entry_text in entries_text]

        # final clean - performs removing stopwords and stemms every word
        clean_entries = []
        for i, entry_only_words in enumerate(entries_only_words):
            words = entry_only_words.lower().split()
            # getDocLength, use all words (this line can be moved around if other lengths (e.g. no stopwords) are used)
            # self.docsLength[i] = len(words) --> normalization done directly in SvenClassifier, there are no stop words
            # if word is not in stopwords, stemm it and save it
            cleaned = [self.stemmer.stem(word) for word in words if word not in self.stop_words]
            # create string from words that passed exam above (words that are not stopwords)
            clean_entries.append(" ".join(cleaned))

        # list of strings separated by space, every string is cleaned text from one text entry in dataset
        return clean_entries

    def get_raw_words(self):
        entries_text = [entry.body.lower() for entry in self.entries]
        return [self.__extract_only_words(entry_text) for entry_text in entries_text]

    def __extract_only_words(self, entry_text):
        return re.sub("[^a-zA-Z0-9]", " ", entry_text)

    def __calcNChars(self, words, sizes):
        for word in words:
            for size in sizes:
                nchars = [word[i:i + size] for i in range(len(word) - size + 1)]
                for nchar in nchars:
                    self.nchars[nchar] = self.nchars.get(nchar, 0) + 1

    def getNChars(self, items, sizes=(2, 3), freq=1):
        entries_text = [entry.body for entry in self.entries]
        entries_only_words = [self.__extract_only_words(entry_text) for entry_text in entries_text]
        for item in entries_only_words:
            self.__calcNChars(item.split(), sizes=sizes)
        return [nchar for nchar, nchar_freq in self.nchars.items() if nchar_freq > freq]

    def labels_for_years(self, year_type):
        text_periods = self.__get_text_periods(year_type)
        labels_lower = []
        labels_upper = []
        for text_period in text_periods:
            time_span = text_period.yes_time_span()
            labels_lower.append(time_span[LOWER])
            labels_upper.append(time_span[UPPER])
        return labels_lower, labels_upper

    def labels_for_years_norm(self, year_type):
        text_periods = self.__get_text_periods(year_type)
        labels_lower = []
        labels_upper = []
        time_span_length = self.__get_time_span_length(text_periods)
        custom_time_spans = self.__generate_custom_time_spans(time_span_length)
        for text_period in text_periods:
            time_span = text_period.yes_time_span()
            chosen_time_span = self.__find_starting_year(time_span, custom_time_spans)
            labels_lower.append(chosen_time_span[LOWER])
            labels_upper.append(chosen_time_span[UPPER])
        return labels_lower, labels_upper

    def __find_starting_year(self, time_span, custom_time_spans):
        intersecs = []  # intersections (amount of years)
        for custom_time_span in custom_time_spans:
            intersec = min(time_span[UPPER], custom_time_span[UPPER]) - max(time_span[LOWER], custom_time_span[LOWER])
            intersecs.append(intersec)
        # take time span for which intersection is largest
        return custom_time_spans[np.argmax(intersecs)]

    def __generate_custom_time_spans(self, time_span_length):
        start = 1700
        spans = []
        while start <= 2012:
            spans.append((start, start + time_span_length))
            start += time_span_length + 1
        return spans

    def __get_time_span_length(self, text_periods):
        time_span = text_periods[0].yes_time_span()
        return time_span[1] - time_span[0]

    def __get_text_periods(self, year_type):
        if year_type is "F":
            return [entry.textF for entry in self.entries]
        if year_type is "C":
            return [entry.textC for entry in self.entries]
        if year_type is "M":
            return [entry.textM for entry in self.entries]