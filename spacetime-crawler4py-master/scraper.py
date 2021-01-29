import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
#import tokenizer
from nltk.tokenize import RegexpTokenizer
import nltk
nltk.download('stopwords')


def scraper(url, resp):
    #check for HTML status code:
    #  we can only check current url since we have current response and status code for that url only
        # less than 200 -> ERROR1
        # 200 to 399(inclusive) -> OK
        # 400+ -> ERROR2
    links = extract_next_links(url, resp)
    result =[]
    soup2 = BeautifulSoup(resp.raw_response.content, 'html5lib')
    # get title 
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
    
    # PUT valid words length and current url stats in website stat file


    
    for link in links:
        if is_valid(link):
            
            
            
            #print(text)
            #tokenize the words (call tokenize function from assignment1)
            result.append(link)
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
