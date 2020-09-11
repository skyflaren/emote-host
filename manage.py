from flask import Flask, request, render_template, send_from_directory, abort, flash, redirect, url_for
import requests, os, magic, platform, copy
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from io import BytesIO

load_dotenv()

EXTENSIONS = ['png','gif','jpg', 'jpeg']
URLS = ['https://aaerialys.cf/emotes']
UPLOAD_FOLDER = os.path.join('%s','static','img')



app = Flask(__name__, static_url_path='')
UPLOAD_FOLDER = UPLOAD_FOLDER % app.root_path
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
		try: return send_from_directory(app.config['UPLOAD_FOLDER'], '%s.%s' % (path, ext))
		except: continue
	return abort(404)


def allowed_filename(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in EXTENSIONS

@app.route('/add', methods=['POST'])
# def upload(id: int) -> str:
def upload():
	submitted_file = request.files['file']
	tmp_file =submitted_file
	f = magic.Magic(mime=True)

	if submitted_file and allowed_filename(submitted_file.filename) and request.form.get("TOKEN") == os.getenv("TOKEN") and (f.from_buffer(tmp_file.read()).split("/")[1] in EXTENSIONS):
		filename = secure_filename(submitted_file.filename)
		directory = app.config['UPLOAD_FOLDER']
		if not os.path.exists(directory):
			os.mkdir(directory)
		submitted_file.save(os.path.join(directory, filename))
		return "Success"
	elif request.form.get("TOKEN") != os.getenv("TOKEN"): return abort(403)
	else: return abort(400)
	

if __name__ == "__main__":
	app.run(debug=True, threaded=True)