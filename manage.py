from flask import Flask, request, render_template, send_from_directory, abort, flash, redirect, url_for
import requests, os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()

EXTENSIONS = ['png','gif','jpg']
URLS = ['https://aaerialys.cf/emotes']
UPLOAD_FOLDER = '/Users/wabasabi/Desktop/emote-host/static/img'



app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
	return render_template("index.html")

@app.route('/<path>')
def fetch(path):
	for link in URLS:
		for ext in EXTENSIONS:
			try: 
				resp = requests.get("%s/%s.%s" % (link, path, ext))
				if resp.status_code >= 400: raise Exception
				return (resp.content, resp.status_code, resp.headers.items())
			except: continue
	for ext in EXTENSIONS:
		try: return send_from_directory('static/img', '%s.%s' % (path, ext))
		except: continue
	return abort(404)


def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in EXTENSIONS

@app.route('/add', methods=['POST'])
# def upload(id: int) -> str:
def upload():
	submitted_file = request.files['file']
	# if submitted_file and allowed_filename(submitted_file.filename) and request.values.tk == os.getenv("TOKEN"):
	if submitted_file and allowed_filename(submitted_file.filename):
		filename = secure_filename(submitted_file.filename)
		directory = app.config['UPLOAD_FOLDER']
		if not os.path.exists(directory):
			os.mkdir(directory)
		submitted_file.save(os.path.join(directory, filename))
	return "Success"

if __name__ == "__main__":
	app.run(debug=True, threaded=True)