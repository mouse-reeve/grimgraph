''' webserver for grimoire graph data '''
from flask import Flask, render_template, request
from graph_service import GraphService
import json

app = Flask(__name__)
graph = GraphService()


# ----- util
def failure(error):
    ''' formats a failure response '''
    return json.dumps({'success': False, 'data': {'error': error}})


def success(data=None):
    ''' formats a success response '''
    return json.dumps({'success': True, 'data': data})


# ----- routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def angular(path):
    ''' render the basic template for angular '''
    return render_template('index.html')


# ----- API routes
@app.route('/api/types', methods=['GET'])
def get_labels():
    ''' list of datatypes that are present '''
    return success(graph.get_labels())

@app.route('/api/<label>', methods=['GET'])
def get_node_list(label):
    ''' load all for a label '''
    data = graph.get_all_for_type(label)
    keys = list(set([item for sublist in data['nodes'] for item in sublist['properties'] \
            if item != 'identifier' and item != 'content']))
    data['properties'] = keys
    return success(data)


@app.route('/api/<label>', methods=['POST'])
def add_node(label):
    ''' create a new item '''
    node_data = request.json
    params = node_data['properties']
    data = graph.add_node(label, params)

    if 'relatedNode' in node_data:
        graph.relate_nodes(node_data['relatedNode'], data[0][0]._id, node_data['relationship'])

    return success()


@app.route('/api/item/<item_id>', methods=['GET'])
def get_node(item_id):
    ''' load a specific item '''
    data = graph.get_node(item_id)
    return success(data)


@app.route('/api/item/<item_id>', methods=['PUT'])
def update_node(item_id):
    ''' create a new item '''
    item = request.json
    node = graph.update_params(item_id, item['properties'])

    return success(node)


@app.route('/api/item/<item1_id>/<item2_id>', methods=['POST'])
def add_relationship(item1_id, item2_id):
    ''' connect two related nodes '''
    rel_name = request.json['relationship']
    graph.relate_nodes(item1_id, item2_id, rel_name)
    return success()

@app.route('/api/rel/<rel_id>', methods=['DELETE'])
def delete_relationship(rel_id):
    ''' delete a rel '''
    graph.remove_relationship(rel_id)
    return success()


if __name__ == '__main__':
    app.debug = True
    app.run(port=4040)
