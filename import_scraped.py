''' upload data from a scrapy web scraper '''
import os
import json
from py2neo import authenticate, Graph
import sys

user = os.environ['NEO4J_USER']
password = os.environ['NEO4J_PASS']
authenticate('localhost:7474', user, password)
graph = Graph()

def add_items(json_file_path, grimoire_id):
    ''' add nodes based on scraped json '''
    with open(json_file_path) as data_file:
        data = json.load(data_file)

        for item in data:
            uid = '-'.join(item['identifier'].lower().split(' ')[:5])
            item['uid'] = uid
            label = item['label']
            del item['label']
            del item['grimoire']

            graph.cypher.execute('CREATE (n:%s {params}) return n' % label, params=item)

if __name__ == '__main__':
    add_items(sys.argv[1], 0)
