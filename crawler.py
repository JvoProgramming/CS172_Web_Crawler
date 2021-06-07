from bs4 import BeautifulSoup
import requests
import time
import uuid
import sys

seedFile = sys.argv[1]
crawlNum = int(sys.argv[2])
crawlNumBackup = crawlNum

queue = [line.rstrip() for line in open(seedFile)]
visited = set()

animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]

while(queue and crawlNum > 0):
    url = queue[0]
    #print("Visited: " + url)
    if url not in visited:
        print("Crawling:", url)
        visited.add(url)
        crawlNum -= 1
    else:
        queue.pop(0)
        continue
    
    try:
        html_content = requests.get(url).text
    except Exception:
        continue
    
    uniqueID = str(uuid.uuid4())
    text_file=open("./crawledFolder/" + uniqueID + '.html', "w", encoding="utf-8")
    text_file.write(html_content)
    text_file.close()

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
            fixedLink = href
        if(fixedLink.endswith("//")):
            fixedLink = fixedLink[:-1]
        if(not fixedLink.endswith("/")):
            fixedLink = fixedLink + '/'
        ########################################
        if fixedLink not in visited:
            queue.append(fixedLink)

    queue.pop(0)
    
    for i in range(len(animation)):
        time.sleep(0.3)
        sys.stdout.write("\r" + animation[i % len(animation)])
        sys.stdout.flush()

    print("\n")

print("Completed scraping", crawlNumBackup, "webpages!")