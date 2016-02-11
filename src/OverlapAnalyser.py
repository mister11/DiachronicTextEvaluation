# Created by svenko11 on 5/5/15 9:47 PM
__author__ = 'Sven Vidak'

from os import listdir
from os.path import isfile, join


def getAllFiles(folder):
	return [join(folder, file) for file in listdir(folder) if isfile(join(folder, file))]


# returns two lists: ids, file in which post appears
def getIds(folder):
	ids = []
	filenames = []
	for filename in getAllFiles(folder):
		file = open(filename, mode='r+', encoding='utf-8')
		for line in file.readlines():
			line = line[1:-1]
			if line.startswith('text id='):
				ids.append(line.split('"')[1])
				filenames.append(file.name)
	return ids, filenames

def mergeToDict(ids, filenames):
	merge = {}
	for (id, filename) in zip(ids, filenames):
		merge.setdefault(id, []).append(filename)
	return merge

def doubles(mergeDict):
	items = []
	for key, value in mergeDict.items():
		if len(value) > 1:
			items.append((key, value))
	return items

if __name__ == '__main__':
	# root is tar_project/src
	folder = '../data/t2data'
	ids, filenames = getIds(folder)
	for f in doubles(mergeToDict(ids, filenames)):
		print(f)