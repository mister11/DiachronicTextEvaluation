# Created by svenko11 on 5/23/15 9:43 PM
__author__ = 'Sven Vidak'

import pickle
import numpy as np

a = np.array([123,574,24234,123,12354,7647,5685,846,345,2345,345,346,3234])

# pickle.dump(a, open('../data/pickles/test1', mode='wb'))

k = pickle.load(open('../data/pickles/train_tag_vecs', mode='rb'))

print(k.shape)