''' upload data from a scrapy web scraper '''
import os
import json
from py2neo import authenticate, Graph
import sys

user = os.environ['NEO4J_USER']
password = os.environ['NEO4J_PASS']
authenticate('localhost:7474', user, password)
graph = Graph()

data = graph.cypher.execute('match (n:grimoire)-[:lists]->(m:spell) where n.uid="long-lost-friend" return m')


for demon in data:
    demon = demon[0]
    content = demon.properties['content']
    quote = '>%s' % content
    sign = '_The Long Lost Friend_, 1820'
    fixed = '%s\n\n%s' % (quote, sign)

    graph.cypher.execute('match (n:spell) where id(n)=%d set n.content={content}' % demon._id, content=fixed)

