__author__ = 'truba'

# enum Type
TYPE_TEXT_F = "<textF"
TYPE_TEXT_M = "<textM"
TYPE_TEXT_C = "<textC"
# end

class ShifterDelegate:
	def evaluate_text(self, text):
		# to be oweridden
		return 1900


class Shifter:
	def __init__(self, type, delegate, test_data=None):
		self.type = type
		self.delegate = delegate
		self.output = 'defOutput.txt'
		self.test_data = test_data


	def perform(self, input_filename, output_filename):
		data = open(input_filename).read()
		self.output = open(output_filename, "w")
		self.start(data)


	def start(self, data):
		index_end = 0
		i = 0
		while True:
			index_start = data.find("<text", index_end)
			index_end = data.find("</text>", index_start)
			if index_start == -1:
				break

			index_start_type = data.find(self.type, index_start)
			index_end_type = data.find(">", index_start_type)

			data = self.__write_year(data, self.test_data[i], index_start_type, index_end_type)

		self.output.write(data)


	def __write_year(self, data, test, index_start_type, index_end_type):
		year = self.delegate.eval_data(test)
		index_no = index_start_type
		while True:
			index_no = data.find("no=\"", index_no, index_end_type)
			if index_no == -1:
				break

			start_year = int(data[index_no + 4:index_no + 8])
			end_year = int(data[index_no + 9:index_no + 13])

			if (year >= start_year) and (year <= end_year):
				data = data[:index_no] + "yes" + data[index_no + 2:]

			index_no += 1

		return data

	def evaluated_replace(self, data, chapter, index_start_type, index_end_type):
		year = self.delegate.evaluate_text(chapter)
		index_no = index_start_type
		while True:
			index_no = data.find("no=\"", index_no, index_end_type)
			if index_no == -1:
				break

			start_year = int(data[index_no + 4:index_no + 8])
			end_year = int(data[index_no + 9:index_no + 13])

			if (year >= start_year) and (year <= end_year):
				data = data[:index_no] + "yes" + data[index_no + 2:]

			index_no += 1

		return data