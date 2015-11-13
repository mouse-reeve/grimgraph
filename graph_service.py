''' neo4j logic '''
from py2neo import Graph

class GraphService(object):
    ''' manage neo4j data operations '''

    def __init__(self):
        self.graph = Graph()


    def add_node(self, data, node_type):
        ''' insert data '''
        pass


    def get_node(self, node_id):
        ''' load data '''
        node = self.graph.cypher.execute('MATCH n  WHERE id(n) = %d RETURN t' % node_id)
        return node


