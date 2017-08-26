from urllib.request import Request, urlopen
import re,json,sys

daftarKataDivs = []
daftarKataColumns = []
startPageId = 1
lastPageId = 1

#Get the html page source of KBBI daftar kata
req = Request('http://kbbi.co.id/daftar-kata', headers={'User-Agent': 'Mozilla/5.0'})
connectionOpen = urlopen(req)
content = connectionOpen.read().decode('utf-8')
connectionOpen.close()

if(len(sys.argv) >= 2):
    #set start page index
    startPageId = (int)(sys.argv[1])

if(len(sys.argv) >= 3):
    #Set the last page index
    lastPageId = (int)(sys.argv[2])
else: 
    #Get the latest page index on the site
    patternLastPageId = re.compile('(\d*?)">Akhir</a>',re.DOTALL)
    lastPageId = (int)(re.findall(patternLastPageId,content)[0])

patternWord = re.compile('<a href="http://.*?kbbi.co.id/arti-kata/.*?">(.*?)</a>',re.DOTALL)
patternLink = re.compile('<a href="(http://[wW\.]*kbbi.co.id/arti-kata/.*?)">.*?</a>',re.DOTALL)
#Get all word in all KBBI daftar kata page and delay preventing connection cut by remote
for pageId in range(startPageId,lastPageId+1):
    print("Getting words in page %d" % (pageId))
    pageAddress = "http://www.kbbi.co.id/daftar-kata?page=%d" % (pageId)
    req = Request(pageAddress, headers={'User-Agent': 'Mozilla/5.0'})
    connectionOpen = urlopen(req)
    content = connectionOpen.read().decode('utf-8')
    connectionOpen.close()
    print ("Saving to Wordlists/Indonesian Wordlist KBBI page %d.txt" % pageId)
    words = re.findall(patternWord,content)
    links = re.findall(patternLink,content)
    wordlist = {}
    for wordId in range(0,len(words)):
        wordlist[words[wordId]] = {
            'name' : words[wordId],
            'link' : links[wordId]
        }
    with open("Wordlists/Indonesian Wordlist KBBI page %d.txt" % pageId, "w") as outfile:
        json.dump(wordlist, outfile)