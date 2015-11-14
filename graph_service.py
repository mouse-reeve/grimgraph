''' neo4j logic '''
from py2neo import Graph

def serialize(func):
    ''' serialize neo4j data '''
    def serialize_wrapper(self, label):
        ''' serialize dis '''
        data = func(self, label)
        serialized = []
        for item in data.records:
            node = item['n']
            serialized.append({
                'id': node._id,
                'labels': [l for l in node.labels],
                'properties': node.properties
            })
        return serialized
    return serialize_wrapper

class GraphService(object):
    ''' manage neo4j data operations '''

    def __init__(self):
        graph = Graph()
        self.query = graph.cypher.execute


    def add_node(self, data, label):
        ''' insert data '''
        pass


    @serialize
    def get_all_for_type(self, label):
        ''' load all nodes with a given label '''
        data = self.query('MATCH (n:%s) RETURN n' % label)
        return data


    def get_node(self, node_id):
        ''' load data '''
        node = self.query('MATCH n WHERE id(n) = %d RETURN t' % node_id)
        return node


