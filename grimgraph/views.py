''' webserver for grimoire graph data '''
from flask import render_template, request
from grimgraph import app, graph
import json


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
    links = [l[0] for l in graph.get_labels()[:3]]
    return render_template('index.html', links=links)


# ----- API routes
@app.route('/api/types', methods=['GET'])
def get_labels():
    ''' list of datatypes that are present '''
    return success(graph.get_labels())

@app.route('/api/types/<label>', methods=['PUT'])
def edit_label(label):
    ''' modify a label '''
    data = request.json
    try:
        updated = data['updated']
    except KeyError:
        return failure('Updated label not found')
    return success(graph.edit_label(label, updated))

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
        graph.relate_nodes(node_data['relatedNode'], \
                           data[0][0]._id, node_data['relationship'])

    return success(data)


@app.route('/api/item/<item_id>', methods=['GET'])
def get_node(item_id):
    ''' load a specific item '''
    data = graph.get_node(item_id)
    common_rels = graph.common_rels(data['nodes'][0]['label'])

    common = [{'rel': c[0], 'label': c[1][0] \
               if not 'parent' in c[1][0] else c[1][1], 'start': True} \
               for c in common_rels['start']]
    common += [{'rel': c[0], 'label': c[1][0] \
                if not 'parent' in c[1][0] else c[1][1], 'start': False} \
                for c in common_rels['end']]

    data['common'] = common
    data['excerpts'] = [n['end']['properties']['content'] \
                        for n in data['relationships']
                        if n['type'] == 'excerpt']

    return success(data)


@app.route('/api/item/<item_id>', methods=['PUT'])
def update_node(item_id):
    ''' create a new item '''
    item = request.json
    node = graph.update_params(item_id, item['properties'])

    return success(node)


@app.route('/api/item/<item_id>', methods=['DELETE'])
def delete_node(item_id):
    ''' create a new item '''
    item_id = int(item_id)
    graph.delete_node(item_id)
    return success()


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


@app.route('/api/query', methods=['POST'])
def run_query():
    ''' create a new item '''
    query = request.json
    data = graph.run_query(query['query'])

    return success(data)
