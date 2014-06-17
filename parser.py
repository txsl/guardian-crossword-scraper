import string

import requests
from bs4 import BeautifulSoup
import tinycss


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
    across_clues[li.span.text] = {}
    across_clues[li.span.text]['clue'] = string.strip(clue)


for li in raw_down.findAll('li'):
    clue = li.text[5:]
    down_clues[li.span.text] = {}
    down_clues[li.span.text]['clue'] = string.strip(clue)


square_size = 29

for div in raw_layout.findAll('div', {'class': 'across'}):

    parser = tinycss.make_parser()
    stylesheet = parser.parse_style_attr(div['style'])

    for dec in stylesheet[0]:
        
        if dec.name == "left":
            left = dec.value[0].value / square_size
        elif dec.name == "top":
            top = dec.value[0].value / square_size
        else:
            pass

    position = left + top*15
    across_clues[div['id'].split('-')[0]]['launch_spot'] = position




for line in str(raw_answers.script).split("\n"):
    if "solutions[" in line:
        separated_answer = line.split('"')

        key = separated_answer[1].split('-')
        res = separated_answer[3]


        # This is reliant on the order of the answers going down the page
        # If not, we have problems. More code would be needed
        try:
            if key[1] == 'across':
                across_clues[key[0]]['answer'] += res
            elif key[1] == 'down':
                down_clues[key[0]]['answer'] += res

        except KeyError:
            if key[1] == 'across':
                across_clues[key[0]]['answer'] = res
            elif key[1] == 'down':
                down_clues[key[0]]['answer'] = res
            


print across_clues, down_clues