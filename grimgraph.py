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
@app.route('/')
def index():
    ''' render start page '''
    return render_template('index.html')


@app.route('/<_>')
def angular(_):
    ''' render the basic template for angular '''
    return render_template('index.html')

# ----- API routes
@app.route('/api/grimoires')
def grimoires():
    ''' load all grimoires '''
    data = graph.get_all_for_type('grimoire')
    return success(data)


if __name__ == '__main__':
    app.debug = True
    app.run(port=4040)
