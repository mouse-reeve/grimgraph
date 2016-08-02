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
            'WHERE m.uid="lesser-key" ' \
            'AND n.content CONTAINS(">") RETURN n'

    data = graph.cypher.execute(query)

    for item in data:
        item = item[0]

        identifier = item.properties['identifier']
        uid = item.properties['uid'] + '-excerpt'
        content = item.properties['content']
        content = re.sub('\n\n_The Lesser Key of Solomon_, Crowley/Mathers edition, 1904', '', content)
        content = re.sub(r'^>', '', content)

        excerpt = {
            'uid': uid,
            'identifier': identifier,
            'content': content,
            'source_title': 'The Lesser Key of Solomon',
            'editor': 'Crowley/Mathers',
            'source_year': 1904,
            'source_url': 'http://www.sacred-texts.com/grim/lks/index.htm'
        }

        query = 'MATCH (n:demon) ' \
                'WHERE n.uid="%s" ' \
                'SET n.content = "" ' \
                'CREATE (e:excerpt {excerpt}) ' \
                'CREATE n-[:excerpt]->e' % item.properties['uid']

        result = graph.cypher.execute(query, excerpt=excerpt)

if __name__ == '__main__':
    add_items()

