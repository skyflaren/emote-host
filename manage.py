from flask import Flask, request, render_template, send_from_directory, abort, flash, redirect, url_for
import requests, os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()

EXTENSIONS = ['png','gif','jpg']
URLS = ['https://dulldesk.github.io/emote-fetcher','https://emot.cf']
UPLOAD_FOLDER = os.path.join('%s','uploads')
ON_404 = "bratwhy"

app = Flask(__name__, static_url_path='')
UPLOAD_FOLDER = UPLOAD_FOLDER % app.root_path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
	return render_template("index.html")

@app.route('/<path>')
def fetch(path):
	path = path.lower()
	for ext in EXTENSIONS:
		try: return send_from_directory(app.config['UPLOAD_FOLDER'], '%s.%s' % (path, ext))
		except: continue
	for link in URLS:
		for ext in EXTENSIONS:
			try: 
				resp = requests.get("%s/%s.%s" % (link, path, ext))
				if resp.status_code >= 400: raise Exception
				return (resp.content, resp.status_code, resp.headers.items())
			except: continue
	
	if path == ON_404: return abort(404)
	return fetch(ON_404)


def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in EXTENSIONS

@app.route('/add', methods=['POST'])
# def upload(id: int) -> str:
def upload():
	submitted_file = request.files['file']
	if submitted_file and allowed_filename(submitted_file.filename) and request.form.get("TOKEN") == os.getenv("TOKEN"):
		filename = secure_filename(submitted_file.filename)
		directory = app.config['UPLOAD_FOLDER']
		if not os.path.exists(directory):
			os.mkdir(directory)
		submitted_file.save(os.path.join(directory, filename))
	elif request.form.get("TOKEN") != os.getenv("TOKEN"): return abort(403)
	else: return abort(400)
	return "Success"

if __name__ == "__main__":
	app.run(threaded=True)
