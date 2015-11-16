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
@app.route('/api/<label>')
def get_node_list(label):
    ''' load all for a label '''
    data = graph.get_all_for_type(label)
    return success(data)


@app.route('/api/<label>', methods=['POST'])
def add_node(label):
    ''' create a new item '''
    params = request.json['properties']
    data = graph.add_node(label, params)

    return success(data)


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


if __name__ == '__main__':
    app.debug = True
    app.run(port=4040)
