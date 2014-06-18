import string

import requests
from bs4 import BeautifulSoup
import tinycss
from lxml import etree


# This is how many pixels occupy each square,
# and tell us which position each crossword starts in
square_size = 29


def get_crossword(id, type='cryptic', format='text'):
    url = "http://www.theguardian.com/crosswords/" + type + "/" + id

    # Get the page
    r = requests.get(url)
    if r.status_code == 404:
        return None

    soup = BeautifulSoup(r.text)

    # Let's grab the Title, Author and Date
    title = soup.find("div", {'id': 'main-article-info'}).h1.text

    article_attributes = soup.find("ul", {'class': 'article-attributes'})

    author = article_attributes.find("li", {'class': 'byline'}).a.text

    # Some more excellent string splitting here ..
    # Reliant on the time always being 00.00
    date = article_attributes.find("li", {'class': 'publication'}).text
    date = string.strip((date.split(','))[1].split('00')[0])

    # We get the clues- and the layout of the clues
    raw_clues_across = soup.find("div", {'class': 'clues-col'})
    raw_clues_down = soup.find("div", {'class': 'clues-col last'})
    raw_layout = soup.find("div", {'id': 'grid'})

    # We're grabbing the 'crossword' div and will grab the solutions
    raw_answers = soup.find("div", {'id': 'wrapper'})
    raw_answers = raw_answers.find("div", {'class': 'crossword'})

    # These dicts are where all clues, locations amd solutions live
    across = {}
    down = {}

    # Populate the clues
    for li in raw_clues_across.findAll('li'):
        # We strip off the start of the string since it has rubbish
        clue = li.text[5:]
        clue_id = li.span.text.split(",")[0]

        # Empty dict for each clue ID
        across[clue_id] = {}

        # Populate the clue with the stripped (cleaned) string
        across[clue_id]['clue'] = string.strip(clue)

    # Same for down
    for li in raw_clues_down.findAll('li'):
        clue = li.text[5:]
        clue_id = li.span.text.split(",")[0]
        down[clue_id] = {}
        down[clue_id]['clue'] = string.strip(clue)

    # We look for each word which is part of the 'across' class
    for div in raw_layout.findAll('div', {'class': 'across'}):

        # We parse the inline styles associated with it
        parser = tinycss.make_parser()
        stylesheet = parser.parse_style_attr(div['style'])

        # Then we go through and pick each useful position out of the styles
        for dec in stylesheet[0]:

            if dec.name == "left":
                left = dec.value[0].value / square_size
            elif dec.name == "top":
                top = dec.value[0].value / square_size
            else:
                pass

        # With those, we can get the position the start of the clue is in
        position = 1 + left + top*15

        # Then save to the correct clue ID
        across[div['id'].split('-')[0]]['launch_spot'] = position

    # Same for down
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

        position = 1 + left + top*15
        # print down
        down[div['id'].split('-')[0]]['launch_spot'] = position

    # Now we collect answers
    for line in str(raw_answers.script).split("\n"):

        # Only interested in lines with the 'solutions' array
        if "solutions[" in line:
            separated_answer = line.split('"')

            # We can get certain values by splitting at strategic locations
            key = separated_answer[1].split('-')
            res = separated_answer[3]

            # This is reliant on the order of the answers going down the page
            # If not, we have problems: More code would be needed

            # If it's the first letter then the value won't exist (key error)
            # If that happens, we start it off with the first letter.

            try:
                if key[1] == 'across':
                    across[key[0]]['answer'] += res
                elif key[1] == 'down':
                    down[key[0]]['answer'] += res

            except KeyError:
                if key[1] == 'across':
                    across[key[0]]['answer'] = res
                elif key[1] == 'down':
                    down[key[0]]['answer'] = res

    # Populate the 'all answers' key
    all_answers = list("-" * 225)

    for key, val in across.iteritems():
        for i in range(len(val['answer'])):
            index = val['launch_spot']
            all_answers[i + index - 1] = val['answer'][i]

    for key, val in down.iteritems():
        for i in range(len(val['answer'])):
            index = val['launch_spot']
            all_answers[i*15 + index - 1] = val['answer'][i]

    all_answers = ''.join(all_answers)

    # Then we start creating the XML
    root = etree.Element('crossword')

    child = etree.Element('Title')
    child.attrib['v'] = title + ', ' + date
    root.append(child)

    child = etree.Element('Author')
    child.attrib['v'] = author
    root.append(child)

    child = etree.Element('Category')
    child.attrib['v'] = "The Guardian Crosswords"
    root.append(child)

    child = etree.Element('Copyright')
    child.attrib['v'] = "The Guardian"
    root.append(child)

    child = etree.Element('Editor')
    child.attrib['v'] = "The Editor"
    root.append(child)

    child = etree.Element('Width')
    child.attrib['v'] = "15"
    root.append(child)

    child = etree.Element('Height')
    child.attrib['v'] = "15"
    root.append(child)

    child = etree.Element('Allanswer')
    child.attrib['v'] = all_answers
    root.append(child)

    # Here we actually add each clue and solution in to the XML
    across_child = etree.Element('across')

    i = 1
    for key, value in across.iteritems():
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
    for key, value in down.iteritems():
        child = etree.Element('d' + str(i))
        child.attrib['a'] = value['answer']
        child.attrib['c'] = value['clue']
        child.attrib['n'] = str(value['launch_spot'])
        child.attrib['cn'] = key
        down_child.append(child)

        i += 1

    root.append(down_child)

    if format == 'etree':
        return root
    else:
        return etree.tostring(root)

if __name__ == "__main__":
    dom = get_crossword('26285',format='etree')
    # The same crossword as http://www.theguardian.com/crosswords/cryptic/26285
    print(etree.tostring(dom, pretty_print=True))
