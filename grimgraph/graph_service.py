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


    @serialize
    def set_label(self, node_id, label, remove=None):
        ''' add or replace labels on a node '''
        query = 'MATCH n WHERE ID(n) = %d SET n:%s' % (node_id, label)
        if remove:
            query += ' REMOVE n:%s' % remove
        query += ' RETURN n'
        return self.query(query)


    def get_labels(self):
        ''' list of all types/labels in the db '''
        data = self.query('MATCH n RETURN DISTINCT LABELS(n), COUNT(n) '
                          'ORDER BY COUNT(n) DESC')
        return [(l[0][0] if not 'parent' in l[0][0] else l[0][1], l[1]) \
                for l in data]


    def edit_label(self, current_label, new_label):
        ''' modify a label by removing it and adding the right text '''
        query = 'MATCH (n:%s) SET n:%s REMOVE n:%s' \
                % (current_label, new_label, current_label)
        self.query(query)
        return self.get_labels()


    @serialize
    def get_all_for_type(self, label):
        ''' load all nodes with a given label '''
        data = self.query('MATCH (n:%s) RETURN n' % label)
        return data


    @serialize
    def get_node(self, node_id):
        ''' load data '''
        node = self.query('MATCH n WHERE id(n) = %s '
                          'OPTIONAL MATCH (n)-[r]-() RETURN n, r' %
                          node_id)
        return node


    def delete_node(self, node_id):
        ''' delete a node that has no rels '''
        query = 'MATCH n WHERE id(n)=%d DELETE n' % node_id
        return self.query(query)


    def relate_nodes(self, node1_id, node2_id, rel_name):
        ''' create a relationship between two nodes '''
        self.query('MATCH n, m WHERE id(n) = %s AND id(m) = %s '
                   'CREATE (n)-[:%s]->(m)' %
                   (node1_id, node2_id, rel_name))


    @serialize
    def add_node(self, label, params):
        ''' insert data '''
        node = self.query('CREATE (n:%s {params}) return n' % label,
                          params=params)
        return node


    def update_params(self, node_id, params):
        ''' set the parameters on a node '''
        self.query('MATCH n WHERE id(n) = %s SET n = {params} RETURN n' %
                   node_id, params=params)

    def remove_relationship(self, rel_id):
        ''' delete rels '''
        return self.query('MATCH ()-[r]-() WHERE id(r) = %s DELETE r' % rel_id)

    def common_rels(self, label):
        ''' a list of relationships that usually exist for a label '''
        start_q = 'MATCH (n:%s)<-[r]-(m) ' \
            'WITH COLLECT(r) AS cr, TYPE(r) AS rs, LABELS(m) AS lm ' \
            'WHERE LENGTH(cr) > 1 RETURN DISTINCT rs, lm' % label
        end_q = 'MATCH (n:%s)-[r]->(m) ' \
            'WITH COLLECT(r) AS cr, TYPE(r) AS rs, LABELS(m) AS lm ' \
            'WHERE LENGTH(cr) > 1 RETURN DISTINCT rs, lm' % label
        return {'start': self.query(start_q), 'end': self.query(end_q)}

    @serialize
    def run_query(self, q):
        ''' run a query for nodes '''
        return self.query(q)
