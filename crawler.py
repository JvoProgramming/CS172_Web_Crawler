#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import time
import uuid
import sys
import re
import string
from urllib.parse import urlparse
from urllib import parse
from urllib import robotparser
import json
import os
import glob

# Function to remove tags
def remove_tags(html):
  
    # parse html content
    soup = BeautifulSoup(html, "html.parser")
  
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
  
    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)

#clears crawledFolder 
os.makedirs("./crawledFolder/", exist_ok=True)

files = glob.glob('./crawledFolder/*')
for f in files:
    os.remove(f)
seedFile = sys.argv[1]
crawlNum = int(sys.argv[2])
crawlNumBackup = crawlNum
parser = robotparser.RobotFileParser()

queue = [line.rstrip() for line in open(seedFile)]

visited = set()

animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]
json_file=open("data.json", "w", encoding="utf-8")

while(queue and crawlNum > 0):
    # 1) Dequeue
    url = queue[0]
    if url not in visited:
        # 2) Check robots.txt
        robotURL = "https://" + urlparse(url).netloc + "/robots.txt"
        try:
            robotContent = requests.get(robotURL).text
            time.sleep(1)
            parser.set_url(parse.urljoin(url, 'robots.txt'))
            parser.read()
            canCrawl = parser.can_fetch("*", "https://" + urlparse(url).netloc)
            if(not canCrawl):
                queue.pop(0)
                continue
        except Exception as e:
            print(e)
            queue.pop(0)
            continue

        print("Crawling:", url)
        #########ADD VARIATIONS TO URL#######
        if(not url.endswith('/')):
            visited.add(url + '/')
            visited.add(url[8:] + '/')
            modifiedURL = url.replace("www.", "")
            visited.add(modifiedURL + '/')
            modifiedURL = url.replace("https://", "")
            visited.add(modifiedURL + '/')
            modifiedURL = url.replace("http://", "")
            visited.add(modifiedURL + '/')
        else:
            visited.add(url)
            visited.add(url[8:])
            modifiedURL = url.replace("www.", "")
            visited.add(modifiedURL)
            modifiedURL = url.replace("https://", "")
            visited.add(modifiedURL)
            modifiedURL = url.replace("http://", "")
            visited.add(modifiedURL)
        #####################################
        crawlNum -= 1
    else:
        queue.pop(0)
        continue
    
    # 3) get HTML and write to file
    try:
        html_content = requests.get(url).text
    except Exception:
        continue
    
    uniqueID = str(uuid.uuid4())
    text_file=open("./crawledFolder/" + uniqueID + '.html', "w", encoding="utf-8")
    text_file.write(html_content)
    page = requests.get(url)
    soup = BeautifulSoup(html_content, "lxml")
    title = soup.find('title')
    if title is None:
        title = "( No Title )"
    else:
        title = '(' + title.string + ')'
    html_text = remove_tags(page.content)
    html_text = html_text.translate(str.maketrans('', '', string.punctuation))
    html_text = re.sub(' +',' ',html_text)
    html_text = html_text.replace("\n", " ")
    html_text = html_text[0:19900]
    json_file.write("{\"index\": {}}\n")
    json_file.write("{\"html\": \"" + title + ' ' + url + ' ' + html_text + "\"}\n")
    text_file.close()


    # 4) extract HTML and add to frontier
    soup = BeautifulSoup(html_content, "lxml")

    for link in soup.find_all("a"):
        href = str(link.get("href"))
        if(href.startswith('#')):
            continue
        ###########TOUCHING UP LINKS############
        if (href.startswith("http") or href.startswith("www")) == False:
            if(href.startswith('/') and len(href) > 1):
                fixedLink = url + href[1:]
                #print(fixedLink)
            else:
                fixedLink = url + href
        else:
            fixedLink = href
        if(fixedLink.endswith("//")):
            fixedLink = fixedLink[:-1]
        if(not fixedLink.endswith("/")):
            fixedLink = fixedLink + '/'
        ########################################
        if fixedLink not in visited:
            queue.append(fixedLink)

    queue.pop(0)
    
    #simple animation taken from https://stackoverflow.com/questions/22029562/python-how-to-make-simple-animated-loading-while-process-is-running
    for i in range(len(animation)):
        time.sleep(0.4)
        sys.stdout.write("\r" + animation[i % len(animation)])
        sys.stdout.flush()

    print("\n")

json_file.close()
print("Completed scraping", crawlNumBackup, "webpages!")

time.sleep(1)

os.system("./indexer.sh")

sys.exit()