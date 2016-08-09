''' upload data from a scrapy web scraper '''
import os
from py2neo import authenticate, Graph
import re

user = os.environ['NEO4J_USER']
password = os.environ['NEO4J_PASS']
authenticate('localhost:7474', user, password)
graph = Graph()

def add_items():
    ''' move Long Lost Friend nodes to excerpt format '''
    query = 'MATCH (m:grimoire)--(n:demon) ' \
            'WHERE m.uid="grand-grimoire" ' \
            'AND n.content CONTAINS("Grand Grimoire") RETURN n'

    data = graph.cypher.execute(query)

    for item in data:
        item = item[0]

        identifier = item.properties['identifier']
        uid = item.properties['uid'] + '-gg-excerpt'
        content = item.properties['content']
        content = re.sub('\n\nGrand Grimoire', '', content)
        content = re.sub(r'"', '', content)

        excerpt = {
            'uid': uid,
            'identifier': identifier,
            'content': content,
            'source_title': 'Grand Grimoire',
            'editor': 'Dark Lodge',
            'source_url': 'http://www.hermetics.org/pdf/grimoire/The%20Grand%20Grimoire%20-%20Dark%20Lodge%20version.pdf'
        }

        query = 'MATCH (n:demon) ' \
                'WHERE n.uid="%s" ' \
                'SET n.content = "" ' \
                'CREATE (e:excerpt {excerpt}) ' \
                'CREATE n-[:excerpt]->e' % item.properties['uid']

        graph.cypher.execute(query, excerpt=excerpt)

if __name__ == '__main__':
    add_items()

