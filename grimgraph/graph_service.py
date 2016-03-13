''' neo4j logic '''
import os
from py2neo import authenticate, Graph
from grimgraph.serializer import serialize

class GraphService(object):
    ''' manage neo4j data operations '''

    def __init__(self):
        user = os.environ['NEO4J_USER']
        password = os.environ['NEO4J_PASS']
        authenticate('localhost:7474', user, password)
        graph = Graph()
        self.query = graph.cypher.execute


    def get_labels(self):
        ''' list of all types/labels in the db '''
        data = self.query('MATCH n RETURN DISTINCT LABELS(n)')
        return [l[0][0] for l in data]


    @serialize
    def get_all_for_type(self, label):
        ''' load all nodes with a given label '''
        data = self.query('MATCH (n:%s) RETURN n' % label)
        return data


    @serialize
    def get_node(self, node_id):
        ''' load data '''
        node = self.query('MATCH n WHERE id(n) = %s OPTIONAL MATCH (n)-[r]-() RETURN n, r' %
                          node_id)
        return node


    def relate_nodes(self, node1_id, node2_id, rel_name):
        ''' create a relationship between two nodes '''
        self.query('MATCH n, m WHERE id(n) = %s AND id(m) = %s CREATE (n)-[:%s]->(m)' %
                   (node1_id, node2_id, rel_name))


    @serialize
    def add_node(self, label, params):
        ''' insert data '''
        node = self.query('CREATE (n:%s {params}) return n' % label, params=params)
        return node


    def update_params(self, node_id, params):
        ''' set the parameters on a node '''
        self.query('MATCH n WHERE id(n) = %s SET n = {params} RETURN n' %
                   node_id, params=params)

    def remove_relationship(self, rel_id):
        ''' delete rels '''
        return self.query('MATCH ()-[r]-() WHERE id(r) = %s DELETE r' % rel_id)
