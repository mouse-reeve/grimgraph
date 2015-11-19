''' webserver for grimoire graph data '''
from flask import Flask, render_template
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
    return render_template('index.html', static='static/readonly')

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


@app.route('/api/item/<item_id>', methods=['GET'])
def get_node(item_id):
    ''' load a specific item '''
    data = graph.get_node(item_id)
    return success(data)


if __name__ == '__main__':
    app.debug = True
    app.run(port=4080)
