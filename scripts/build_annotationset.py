''' create a key/value dict for text annotations '''
import os
import json
from py2neo import authenticate, Graph

user = os.environ['NEO4J_USER']
password = os.environ['NEO4J_PASS']
authenticate('localhost:7474', user, password)
graph = Graph()
query = graph.cypher.execute

labels = query('MATCH n RETURN DISTINCT LABELS(n)')
labels = [[m for m in list(l)[0] if not 'parent' in m][0] for l in labels]
labels = list(set(labels))

skip = ['excerpt', 'image', 'event', 'spell']
labels = [l for l in labels if not l in skip]

annotations = {}
for label in labels:
    nodes = query('MATCH (n:%s) RETURN n' % label)
    for node in nodes:
        node = node[0]
        url = '/%s/%s' % (label, node.properties['uid'])
        words = [node.properties['uid'], node.properties['identifier'].lower()]
        if 'alternate_names' in node.properties:
            alts = node.properties['alternate_names'].split(', ')
            words += [w.lower() for w in alts]
        for word in words:
            annotations[word] = url

print json.dumps(annotations)
