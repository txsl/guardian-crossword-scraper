import string

from bs4 import BeautifulSoup
import requests

url = "http://www.theguardian.com/crosswords/cryptic/26288"

r = requests.get(url)

soup = BeautifulSoup(r.text)

raw_across = soup.find("div", {'class':'clues-col'})
raw_down = soup.find("div", {'class':'clues-col last'})
raw_layout = soup.find("div", {'id': 'grid'})

raw_answers = soup.find("div", {'id':'wrapper'})
raw_answers = raw_answers.find("div", {'class': 'crossword'})

# print raw_answers.script
# exit()


# print raw_down
# print '============================================='
# print raw_across

across_clues = {}
down_clues = {}

for li in raw_across.findAll('li'):
    clue = li.text[5:]
    across_clues[li.span.text] = string.strip(clue)


for li in raw_down.findAll('li'):
    clue = li.text[5:]
    down_clues[li.span.text] = string.strip(clue)

print across_clues
print down_clues

print raw_layout