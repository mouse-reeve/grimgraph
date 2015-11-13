''' webserver for grimoire graph data '''
from flask import Flask, render_template

app = Flask(__name__)

# ----- routes
@app.route('/')
def index():
    ''' render start page '''
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run(port=4040)
