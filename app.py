import subprocess
from flask import Flask, render_template
from shutil import copyfile
from gevent.pywsgi import WSGIServer

app = Flask(__name__, static_url_path='', static_folder='web/static', template_folder='web/views')
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/name/<name>")
def name(name):
    return render_template('index.html', name=name)

if __name__ == "__main__":
	# Generate the Brython modules
	subprocess.check_output(['brython-cli', '--modules'], cwd="./web/views")
	copyfile("./web/views/brython.js", "./web/static/js/brython.js")
	copyfile("./web/views/brython_stdlib.js", "./web/static/js/brython_stdlib.js")
	copyfile("./web/views/brython_modules.js", "./web/static/js/brython_modules.js")

	# Start the gevent WSGI server
	http_server = WSGIServer(('127.0.0.1', 5000), app)
	http_server.serve_forever()
