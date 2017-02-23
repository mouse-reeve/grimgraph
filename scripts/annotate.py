''' add links to a block of text '''
import json
import re

annotation_set = json.load(file('scripts/annotation_set.json'))
original = open('verum.md', 'r')

annotated = original.read()
for word in annotation_set:
    utf_word = word.encode('utf8')
    link = annotation_set[word].encode('utf8')
    annotated = re.sub(r'\b(%s)\b' % utf_word,
                       r'[XXXDONEXXX\1](%s)' % link,
                       annotated,
                       flags=re.IGNORECASE)

annotated = re.sub('XXXDONEXXX', '', annotated)

open('verum-annotated.md', 'w').write(annotated)


