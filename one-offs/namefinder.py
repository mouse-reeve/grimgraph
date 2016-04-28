''' search for entity names in text
But right now it justs prints a list of all words '''
import sys

def process(text):
    text = text.lower()
    words = text.split(' ')
    words = set(words)
    words = list(words)
    words.sort()
    print '\n'.join(words)

if __name__ == '__main__':
    grimoire = open(sys.argv[1], 'r')
    process(grimoire.read())

