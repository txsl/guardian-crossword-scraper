import string

import requests
from bs4 import BeautifulSoup
import tinycss
from lxml import etree

def get_crossword(id, type='cryptic'):

    url = "http://www.theguardian.com/crosswords/" + type + "/" + id

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
        clue_id = li.span.text.split(",")[0]
        down_clues[clue_id] = {}
        down_clues[clue_id]['clue'] = string.strip(clue)


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

    for div in raw_layout.findAll('div', {'class': 'down'}):

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
        # print down_clues
        down_clues[div['id'].split('-')[0]]['launch_spot'] = position




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
                


    # print across_clues, down_clues


    root = etree.Element('crossword')

    child = etree.Element('Title')
    child.attrib['v'] = "This title doesn't appear"
    root.append(child)

    child = etree.Element('Author')
    child.attrib['v'] = "AUTHOR"
    root.append(child)

    child = etree.Element('Category')
    child.attrib['v'] = "The Guardian Crosswords"
    root.append(child)

    child = etree.Element('Copyright')
    child.attrib['v'] = "The Guardian"
    root.append(child)

    child = etree.Element('Editor')
    child.attrib['v'] = "EDITOR"
    root.append(child)

    child = etree.Element('Width')
    child.attrib['v'] = "15"
    root.append(child)

    child = etree.Element('Height')
    child.attrib['v'] = "15"
    root.append(child)


    across_child = etree.Element('across')

    i = 1
    for key, value in across_clues.iteritems():
        child = etree.Element('a' + str(i))
        child.attrib['a'] = value['answer']
        child.attrib['c'] = value['clue']
        child.attrib['n'] = str(value['launch_spot'])
        child.attrib['cn'] = key
        across_child.append(child)

        i += 1

    root.append(across_child)


    down_child = etree.Element('down')

    i = 1
    for key, value in down_clues.iteritems():
        child = etree.Element('d' + str(i))
        child.attrib['a'] = value['answer']
        child.attrib['c'] = value['clue']
        child.attrib['n'] = str(value['launch_spot'])
        child.attrib['cn'] = key
        down_child.append(child)

        i += 1

    root.append(down_child)

    s = etree.tostring(root)

    return s
