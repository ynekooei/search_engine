import pickle
from collections import defaultdict
from operator import itemgetter

#### CONTAINS MOST COMMON WORDS SORT AND DISPLAY LARGEST 50 BY VALUE
word_frequency = defaultdict(int)
with open('stats_word_frequency.pickle', 'rb') as handle:
    word_frequency = pickle.load(handle)

sorted_word_frequency = dict(sorted(word_frequency.items(), key=lambda item: item[1],reverse=True))
sorted_word_frequency_items = sorted_word_frequency.items()
most_common_words = list(sorted_word_frequency_items)[:50] 

### FOR URL WITH MOST WORDS
url_word_length = defaultdict(int)
with open('stats_word_count.pickle', 'rb') as handle:
    url_word_length = pickle.load(handle)
sorted_dict_count= dict(sorted(url_word_length.items(), key=lambda item: item[1],reverse=True))
sorted_dict_count_items = sorted_dict_count.items()
first = list(sorted_dict_count_items)[:1] 
#print(first)  #first contains url with most words plus word count

# UNIQUE URLS
unique_urls = defaultdict(int)
with open('unique_urls.pickle', 'rb') as handle:
    unique_urls = pickle.load(handle)

#subdomains
subdomains = defaultdict(int)
with open('unique_domains.pickle', 'rb') as handle:
    subdomains = pickle.load(handle)
sorted_subdomains= dict(sorted(subdomains.items(), key=lambda item: item[0],reverse=False))
sorted_subdomains_items = sorted_subdomains.items()
all_subdomains = list(sorted_subdomains_items)[0:] 
print(str(all_subdomains))

with open('project2_stats.txt','w') as writer:
    writer.write("Number of unique pages: " + str(len(unique_urls)) + "\n")
    writer.write("Longest page: " + str(first) +"\n")
    writer.write("50 most common words")
    for j in range(len(most_common_words)):
        writer.write(str(most_common_words[i]) + "\n")
    writer.write("subdomains found: " + str(len(subdomains)) + "\n")
    for i in range(len(all_subdomains)):
        writer.write(str(all_subdomains[i]) + "\n")
        
       
