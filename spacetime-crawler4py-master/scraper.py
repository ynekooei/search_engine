import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def scraper(url, resp):
    links = extract_next_links(url, resp)
    
    return [link for link in links if is_valid(link)]
    

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
        #check if the domain (netloc) and path are valid (match the 5 expected URLds)
        if (not (re.match(r"(.+\.ics\.uci\.edu$)|(.+\.cs\.uci\.edu$)" | r"|(.+\.informatics\.uci\.edu$)|(.+\.stat\.uci\.edu$)", parsed.netloc)
            | (re.match(r"^today\.uci\.edu$", parsed.netloc) & re.match(r"\/department\/information_computer_sciences(\/.+|$)", parsed.path)))):
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
