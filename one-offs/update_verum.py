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
            name = item['name'][0] + item['name'][1:].lower()
            content = item['description'] + '\n\n_Grimorium Verum_'
            nodes = graph.cypher.execute('match (n:demon) where n.uid =~ "(?i)%s" or "%s" in n.alternate_names return n' % (name, name))

            graph.cypher.execute('match (n:demon) where id(n)=%d set n.content={content} set n.source="http://www.hermetics.org/pdf/grimoire/Grimoirum_Verum.pdf"' % nodes[0][0]._id, content=content)

if __name__ == '__main__':
    add_items(sys.argv[1], 0)
