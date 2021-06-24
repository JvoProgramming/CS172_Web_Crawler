# CS172_Web_Crawler
(WINDOWS INSTRUCTIONS)
Requires NodeJS (for server) and install all packages required by running: npm install
Modules required: 
    CORS, 
    express,
    @elastic/elastic

Start the server by running: node server.js

In seed.txt, fill it up with your desired seed URLs

To run the python script, execute (in the terminal): py ./crawler.py <seed file name> <number of webpages to crawl>
*note: type the command without the brackets*
For example: py ./crawler.py seed.txt 10 would insert all the links in seed.txt into the queue and then crawl 10 pages. 

To change the speed of the crawler, adjust time.sleep() by a tenth, either higher (slower) or lower (faster)

After the crawler is done running, it automatically executes the indexer.

If you wish to run the indexer by itself, execute (in the terminal): ./indexer.sh

VIDEO DEMO: https://drive.google.com/file/d/1Ot1WQFGY9MMDmSQa__HsCHfo6ErFAhk3/view?usp=sharing
