from bs4 import BeautifulSoup
import requests
import time
import uuid
import sys
import re
from urllib.parse import urlparse
from urllib import parse
from urllib import robotparser
import json

seedFile = sys.argv[1]
crawlNum = int(sys.argv[2])
crawlNumBackup = crawlNum
parser = robotparser.RobotFileParser()

queue = [line.rstrip() for line in open(seedFile)]

visited = set()

animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]

while(queue and crawlNum > 0):
    # 1) Dequeue
    url = queue[0]
    if url not in visited:
        # 2) Check robots.txt
        robotURL = "https://" + urlparse(url).netloc + "/robots.txt"
        try:
            robotContent = requests.get(robotURL).text
            parser.set_url(parse.urljoin(url, 'robots.txt'))
            parser.read()
            canCrawl = parser.can_fetch("*", "https://" + urlparse(url).netloc)
            if(not canCrawl):
                queue.pop(0)
                continue
        except Exception:
            continue

        print("Crawling:", url)
        visited.add(url)
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
    text_file.close()


    # 4) extract HTML and add to frontier
    soup = BeautifulSoup(html_content, "lxml")

    for link in soup.find_all("a"):
        href = str(link.get("href"))
        ###########TOUCHING UP LINKS############
        if (href.startswith("http") or href.startswith("www")) == False:
            if(href.startswith('/') and len(href) > 1):
                fixedLink = url + href[1:]
                #print(fixedLink)
            else:
                fixedLink = url + href
        else:
            if url.startswith('http'):
                fixedLink = re.sub(r'https?:\\', '', url)
            if url.startswith('www.'):
                fixedLink = re.sub(r'www.', '', url)
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
        time.sleep(0.3)
        sys.stdout.write("\r" + animation[i % len(animation)])
        sys.stdout.flush()

    print("\n")

print("Completed scraping", crawlNumBackup, "webpages!")