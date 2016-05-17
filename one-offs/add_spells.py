''' upload data from a scrapy web scraper '''
import os
import json
from py2neo import authenticate, Graph
import re
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
            identifier = re.sub(r'[\.,]', '', item['title'])
            uid = re.sub(r'[\':]', '', identifier).lower().split(' ')
            skipwords = ['to', 'for', 'that', 'of', 'the', 'how', 'and', 'it', 'a', 'should',
                         'be', 'that']
            uid = [i for i in uid if not i in skipwords]

            uid = '-'.join(uid[:5]) + '-esam'

            content = item['content']

            node = {
                'uid': uid,
                'identifier': identifier
            }

            excerpt = {
                'uid': uid + '-excerpt',
                'identifier': item['title'],
                'content': content,
                'source_year': 2006,
                'editor': 'Joseph H. Peterson',
                'source_title': 'Egyptian Secrets of Albertus Magnus',
                'source_url': 'http://esotericarchives.com/moses/egyptian.htm'
            }

            query = 'MATCH (n:grimoire) ' \
                    'WHERE n.uid="egyptian-secrets-of-albertus-magnus" ' \
                    'CREATE (s:spell {spell}) ' \
                    'CREATE (e:excerpt {excerpt}) ' \
                    'CREATE n-[:lists]->s ' \
                    'CREATE s-[:excerpt]->e'

            graph.cypher.execute(query, spell=node, excerpt=excerpt)

if __name__ == '__main__':
    add_items(sys.argv[1])

