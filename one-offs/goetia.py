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
            name = item['name'].lower()
            description = '"%s"\n\nThe Lesser Key of Solomon, Crowley/Mathers edition, 1904' % item['description']

            q = 'MATCH (n:demon) WHERE n.identifier =~ {term} OR n.alternate_names =~ {term} RETURN n'
            nodes = graph.cypher.execute(q, term='(?i).*%s.*' % name)
            if len(nodes) == 1:
                node = nodes[0][0]
                graph.cypher.execute('MATCH n where id(n)=%d set n.content={content} set n.source="https://archive.org/details/ac_goetia"' % (node._id), content= description )
            else:
                print name
                print description
                print ''


if __name__ == '__main__':
    add_items(sys.argv[1], 0)
