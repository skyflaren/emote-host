from flask import Flask, redirect, url_for, render_template, request, send_from_directory, abort, make_response
import requests

app = Flask(__name__, static_url_path='')

extensions = ['png','gif']
urls = ['https://aaerialys.cf/emotes']

@app.route("/")
def home():
	return send_from_directory('img', 'poggies.png')

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
		try: return send_from_directory('img', '%s.%s' % (path, ext))
		except: continue
	return abort(404)

if __name__ == "__main__":
	app.run(debug=True)