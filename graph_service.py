''' neo4j logic '''
import json
from py2neo import Graph

def serialize(func):
    ''' serialize neo4j data '''
    def serialize_wrapper(self, label):
        ''' serialize dis '''
        data = func(self, label)
        nodes = []
        rels = []
        for item in data.records:

            try:
                item_rels = item['r']
            except AttributeError:
                pass
            else:
                for rel in item_rels:
                    rels.append({
                        'id': rel._id,
                        'start': {
                            'id': rel.start_node._id,
                            'labels':  [l for l in rel.start_node.labels],
                            'properties': rel.start_node.properties
                        },
                        'end': {
                            'id': rel.end_node._id,
                            'labels':  [l for l in rel.end_node.labels],
                            'properties': rel.end_node.properties
                        },
                        'type': rel.type,
                        'properties': rel.properties
                    })
            try:
                node = item['n']
            except AttributeError:
                pass
            else:
                nodes.append({
                    'id': node._id,
                    'labels': [l for l in node.labels],
                    'properties': node.properties,
                })

        return {'nodes': nodes, 'relationships': rels}
    return serialize_wrapper

class GraphService(object):
    ''' manage neo4j data operations '''

    def __init__(self):
        graph = Graph()
        self.query = graph.cypher.execute


    @serialize
    def get_all_for_type(self, label):
        ''' load all nodes with a given label '''
        print('MATCH (n:%s) RETURN n' % label)
        data = self.query('MATCH (n:%s) RETURN n' % label)
        return data


    @serialize
    def get_node(self, node_id):
        ''' load data '''
        node = self.query('MATCH n-[r]-() WHERE id(n) = %s RETURN n, r' % node_id)
        return node


    def add_node(self, label, params):
        ''' insert data '''
        node = self.query('CREATE (n:%s) %s return n' % (label, json.dumps(params)))
        return node


    def update_params(self, node_id, params):
        ''' set the parameters on a node '''
        self.query('MATCH n WHERE id(n) = %s SET n = {params} RETURN n' %
                   node_id, params=params)
