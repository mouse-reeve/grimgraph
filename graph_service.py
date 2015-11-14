''' neo4j logic '''
from py2neo import Graph

def serialize(func):
    ''' serialize neo4j data '''
    def serialize_wrapper(self, label):
        ''' serialize dis '''
        data = func(self, label)
        serialized = []
        for item in data.records:
            node = item['node']
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
        data = self.query('MATCH (node:%s) RETURN node' % label)
        return data


    @serialize
    def get_node(self, node_id):
        ''' load data '''
        node = self.query('MATCH node WHERE id(node) = %s RETURN node' % node_id)
        return node


