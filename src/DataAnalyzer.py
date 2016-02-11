# Created by mister11 on 4/7/15 338 PM
__author__ = 'Sven Vidak'

from Preprocessor import Preprocessor

_18th_cent = 0
_19th_cent = 1
_20th_cent = 2
_21th_cent = 3


class DataAnalyzer:
	def __init__(self, *filenames):
		self.preprocessor = Preprocessor(*filenames)
		self.preprocessor.clean_entries()

	def get_posts_by_centuries(self):
		data = {_18th_cent: {}, _19th_cent: {}, _20th_cent: {}, _21th_cent: {}}
		for entry in self.preprocessor.entries:
			century = self.__get_century(entry.textF.yes_time_span())
			if century is not None:
				self.__parseEntry(data, century, entry.body)
		return data

	def __get_century(self, time_span):
		century_start, century_end = time_span[0] // 100, time_span[1] // 100
		if (century_start == 16 or century_start == 17) and (century_end == 16 or century_end == 17):
			return _18th_cent
		if century_start == century_end:
			if century_start == 18:
				return _19th_cent
			elif century_start == 19:
				return _20th_cent
			elif century_start == 20:
				return _21th_cent
			else:
				return None
		else:
			return None

	def __parseEntry(self, data, century, body):
		tokens = body.split()
		for token in tokens:
			data[century][token] = data[century].get(token, 0) + 1


if __name__ == '__main__':
	d = DataAnalyzer('../data/training08T2.txt')
	data = d.get_posts_by_centuries()
	for key in data.keys():
		print(sorted(data.get(key).items(), key=lambda x: x[1], reverse=True))