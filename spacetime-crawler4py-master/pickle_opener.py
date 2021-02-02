import pickle
from collections import defaultdict
from operator import itemgetter

word_frequency = defaultdict(int)
with open('stats_word_frequency.pickle', 'rb') as handle:
    word_frequency = pickle.load(handle)

#sort_dict= dict(sorted(word_frequency.items(), key=lambda item: item[1],reverse=True))
#print(sort_dict)


url_word_length = defaultdict(int)
with open('stats_word_count.pickle', 'rb') as handle:
    url_word_length = pickle.load(handle)

sort_dict_count= dict(sorted(url_word_length.items(), key=lambda item: item[1],reverse=True))
print(sort_dict_count)
