from flask import Flask, request, render_template, send_from_directory, abort
import requests, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_url_path='')

extensions = ['png','gif','jpg']
urls = ['https://aaerialys.cf/emotes']

@app.route("/")
def home():
	return render_template("index.html")

@app.route('/<path>')
def fetch(path):
	for link in urls:
		for ext in extensions:
			try: 
				resp = requests.get("%s/%s.%s" % (link, path, ext))
				if resp.status_code >= 400: raise Exception
				return (resp.content, resp.status_code, resp.headers.items())
			except: continue
	for ext in extensions:
		try: return send_from_directory('static/img', '%s.%s' % (path, ext))
		except: continue
	return abort(404)

if __name__ == "__main__":
	app.run()
