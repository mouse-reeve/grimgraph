''' upload data from a scrapy web scraper '''
import os
import json
from py2neo import authenticate, Graph
import sys

user = os.environ['NEO4J_USER']
password = os.environ['NEO4J_PASS']
authenticate('localhost:7474', user, password)
graph = Graph()

def add_items(json_file_path):
    ''' add nodes based on scraped json '''
    with open(json_file_path) as data_file:
        data = json.load(data_file)

        for item in data:
            uid = item['identifier'].lower().split(' ')
            skipwords = ['to', 'for', 'that', 'of', 'the', 'how', 'and', 'it', 'a', 'should',
                         'be', 'that']
            uid = [i for i in uid if not i in skipwords]

            uid = '-'.join(uid[:5]) + '-kos'
            item['uid'] = uid
            text = '\n>\n> '.join(item['text'].split('\n'))
            item['content'] = '_The Key of Solomon_, Mathers\' edition (1888):\n\n> %s' % text
            label = item['label']
            del item['label']
            del item['grimoire']
            del item['text']

            print item
            #graph.cypher.execute('CREATE (n:%s {params}) return n' % label, params=item)

if __name__ == '__main__':
    add_items(sys.argv[1])
