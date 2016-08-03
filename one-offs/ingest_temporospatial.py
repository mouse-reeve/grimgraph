''' upload data from a scrapy web scraper '''
import os
import json
from py2neo import authenticate, Graph
import re

user = os.environ['NEO4J_USER']
password = os.environ['NEO4J_PASS']
authenticate('localhost:7474', user, password)
graph = Graph()

data = json.load(open('one-offs/temporospatial.json'))

for item in data:
    uid = re.sub(' of', '', item['description'])
    uid = re.sub(' the', '', uid)
    uid = re.sub('\'', '', uid)
    uid = re.sub(' ', '-', uid)
    uid = uid.lower()

    event = {
        'identifier': item['description'],
        'uid': uid,
        'latitude': item['latitude'],
        'longitude': item['longitude'],
        'location': item['location_name'],
        'location_precision': item['location_precision'],
        'date': item['date'],
        'date_precision': item['date_precision'],
        'event': item['event_type']
    }
    query = 'MATCH n where id(n) = %s ' \
            'CREATE (e:event {event}) ' \
            'CREATE n-[:event]->e' % item['node_id']
    graph.cypher.execute(query, event=event)
