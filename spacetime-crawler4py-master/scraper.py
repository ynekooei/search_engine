import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
#import tokenizer



def scraper(url, resp):
    links = extract_next_links(url, resp)
    result =[]
    for link in links:
        if is_valid(link):
            #figure out how to extract 'valuable' text
            #soup2 = BeautifulSoup(resp.raw_response.content, 'html5lib')
            #text = soup2.find_all("p")
            #print(text)
            #tokenize the words (call tokenize function from assignment1)
            result.append(link)
    return result
    

def extract_next_links(url, resp):
    # Implementation requred.
    list = []
    #print(resp.raw_response.text[0:500])
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
        
        #check for HTML status code:
        # less than 200 -> ERROR1
        # 200 to 399(inclusive) -> OK
        # 400+ -> ERROR2
        


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
