#!/usr/bin/python

import re

from collections import Counter, defaultdict
from lxml import etree

from pprint import pprint

doc = etree.parse("data/BJNR036710013.xml")
words_map = dict(
    ist='sein', bin='sein', sind='sein', seid='sein',
    die='der', das='der', den='der', dem='der', des='der',
    eine='ein', einen='ein', einem='ein', einer='ein', eines='ein',
    zum='zu', zur='zu',
    im='in',
    vom='von',
    am='an',
    hat='haben', 
)

ignored_re = [
    '^\s*[§…–]\s*$', '^\s*\d+([.,]\d+|[)]|\w)?\s*$', '^\w$', '^\d+/\d+/\d+$',
]

root = doc.getroot()
#print(root, root.tag, root.keys(), root.items())
#for norm in root.getchildren():
#    #print(norm, norm.tag, norm.keys(), norm.items())
#    for data in norm.getchildren():
#        print(data.tag)
#        if data.tag == 'metadaten':
#            try:
#                print(data.titel)
#            except AttributeError:
#                pass
#        if data.tag == 'textdaten':
#            print(data.text)
#    #break

#def get_child(element, child_tag):
#    if element.g

def get_text(element):
    text = element.text or ''
    #print(element.tag, text)

    for child in element.getchildren():
        join_str = ''

        if child.tag in ('P', 'row', 'BR', 'entry', 'DD', 'DT') and text != '':
            join_str = '\n'

        text = join_str.join([text, get_text(child)])

    return text

def map_word(word):
    mapped_word = word.lower()

    if mapped_word in words_map:
       mapped_word = words_map[mapped_word]

    return mapped_word

def sanitize_word(word):
    sanitized_word = word
    sanitized_word = re.sub('[,.)]$', '', sanitized_word)
    sanitized_word = re.sub('^[(]', '', sanitized_word)
    sanitized_word = map_word(sanitized_word)
    return sanitized_word

def match_ignored(word):
    for regexp in ignored_re:
        if re.match(regexp, word, re.I) is not None:
            return True

    return False

def parse_text(element, result):
    #re_words = re.compile('
    #update

    if element.tag == 'norm':
        title = element.find('metadaten/titel')
        content = element.find('textdaten/text/Content')
        if content is not None:
            text = get_text(content)
            words = [ word for word in map(sanitize_word, text.split()) if match_ignored(word) == False ]
            result['stat']['words'].update(words)
        return 'norm'
        
    for child in element.getchildren():
        parse_text(child, result)

text = defaultdict(dict)
text['stat']['words'] = Counter()

parse_text(root, text)
print(len(text['stat']['words']))
print(sum(text['stat']['words'].values()))
pprint(text)

#print(root.findall('titel'))

#i = doc.getiterator()
#
#for e in i:
#    print(e.tag, e.items(), e.getchildren(), e.get('text'))

