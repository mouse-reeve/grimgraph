import csv
import os
from py2neo import Graph, Node, authenticate

user = os.environ['NEO4J_USER']
password = os.environ['NEO4J_PASS']
authenticate('localhost:7474', user, password)
graph = Graph()

with open('../grimoires/raw-data/grimoires.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    header = True
    for row in reader:
        if header:
            header = False
            continue
        try:
            century = str(int(row[6]) - 1) + '00'
        except ValueError:
            century = ''
        data = {
            'identifier': row[1],
            'uid': row[0],
            'century': century,
            'decade': row[7],
            'year': row[8]
        }

        node = Node("grimoire")
        node.set_properties(data)
        graph.create(node)
