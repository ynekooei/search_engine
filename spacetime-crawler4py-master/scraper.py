import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
#import tokenizer
from nltk.tokenize import RegexpTokenizer
import nltk
nltk.download('stopwords')
from collections import defaultdict
import pickle


def scraper(url, resp):
    #check for HTML status code:
    
    links = extract_next_links(url, resp)
    result =[]

    if ((resp.status < 200) or (resp.status > 399) or (resp.raw_response is None) or (resp.raw_response.content == "")):
        return result

    soup2 = BeautifulSoup(resp.raw_response.content, 'html5lib')
    # get title
    text = ""
    if soup2.title != None: 
        text = soup2.title.get_text()
    
    for x in soup2.find_all('p'):
        text += x.get_text()
    
    tokenizer = RegexpTokenizer('\w+')
    tokens = tokenizer.tokenize(text)
    valid_words = []
    stopwords = nltk.corpus.stopwords.words('english')

    for word in tokens:
        if word not in stopwords:
            valid_words.append(word.lower())
    
    # compute hash (simhash) using valid_words and check againsts previous hashes for page similarity
    # if the same then return empty list otherwise, proceed        
    
    # put valid words length and current url stats in website stat dictionary
    url_word_length = defaultdict(int)
    try:
        with open('stats_word_count.pickle', 'rb') as handle:
            url_word_length = pickle.load(handle)
    except (OSError, IOError) as e:
       pickle.dump(url_word_length, open('stats_word_count.pickle', "wb"))

    url_word_length[url] = len(valid_words)
    
    with open('stats_word_count.pickle', 'wb') as handle:
        pickle.dump(url_word_length, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    


    word_frequency = defaultdict(int)
    #load word frequencies using pickle
    try:
        with open('stats_word_frequency.pickle', 'rb') as handle:
            word_frequency = pickle.load(handle)
    except (OSError, IOError) as e:
        pickle.dump(word_frequency, open('stats_word_frequency.pickle', "wb"))

    #update word_frequency file 
    for word in valid_words: 
        word_frequency[word] += 1


    
    #store word_frequency into file
    with open('stats_word_frequency.pickle', 'wb') as handle:
        pickle.dump(word_frequency, handle, protocol=pickle.HIGHEST_PROTOCOL)

    #with open('stats_word_frequency', 'rb') as handle:
        #word_frequency = pickle.load(handle)


    
    for link in links:
        if is_valid(link):
            # remove link fragments
            new_link= link.split('#')[0]
            
            
            #print(text)
            #tokenize the words (call tokenize function from assignment1)
            result.append(new_link)
    return result
    

def extract_next_links(url, resp):
    # Implementation requred.
    list = []
    
    if resp.raw_response is None:
        return list
    soup = BeautifulSoup(resp.raw_response.content, 'html5lib')

    #print(soup.prettify())
    #for a in soup.find_all('a', href=True):
     #   print ("Found the URL:", a['href'])
    
    for a in soup.find_all('a', href=True):
        list.append(a['href'])

    
    return list

def is_valid(url):
    try:
        parsed = urlparse(url)
        
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        
        


        #check if the domain (netloc) and path are valid (match the 5 expected URLds)
        if (not (re.match(r"(.+\.ics\.uci\.edu$)|(.+\.cs\.uci\.edu$)"
                + r"|(.+\.informatics\.uci\.edu$)|(.+\.stat\.uci\.edu$)", parsed.netloc)
            or (re.match(r"^today\.uci\.edu$", parsed.netloc) and 
                re.match(r"\/department\/information_computer_sciences(\/.+|$)", parsed.path)))):
            return False


        if (re.match(r"^evoke.ics.uci.edu", parsed.netloc) and re.search(r"replytocom=[a-zA-Z0-9]+(\/$|$)", parsed.query)):
            return False  
        
        #to avoid the calendar trap: calendar.ics.uci.edu OR http://calendar.ics.uci.edu/calendar.php?type=month&calendar=1&category=&month=02&year=2013
        # (CHECK) ??
        if (re.match(r"calendar\.ics\.uci\.edu",parsed.netloc)):
            return False
        
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
