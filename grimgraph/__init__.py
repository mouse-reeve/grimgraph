""" webserver for grimgraph graph data """
from flask import Flask

from grimgraph.graph_service import GraphService

app = Flask(__name__)
app.config.from_object('config')

graph = GraphService()

import grimgraph.views
