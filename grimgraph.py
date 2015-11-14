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
    return render_template('index.html')

# ----- API routes
@app.route('/api/<label>')
def item_list(label):
    ''' load all for a label '''
    data = graph.get_all_for_type(label)
    return success(data)


@app.route('/api/item/<item_id>')
def item(item_id):
    ''' load a specific item '''
    data = graph.get_node(item_id)
    return success(data[0])

if __name__ == '__main__':
    app.debug = True
    app.run(port=4040)
