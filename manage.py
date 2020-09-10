from flask import Flask, redirect, url_for, render_template, request, send_from_directory

app = Flask(__name__, static_url_path='')


@app.route("/")
def home():
	return send_from_directory('img', 'poggies.png')

@app.route('/<path>')
def fetch(path):
	path += ".png"
	return send_from_directory('img', path)

if __name__ == "__main__":
	app.run(debug=True)