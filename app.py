import flask 

app = flask.Flask(__name__, template_folder='views')

@app.route('/')
def home():
    return flask.render_template('index.html')