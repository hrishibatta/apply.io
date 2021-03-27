from flask import Flask, flash, redirect, render_template, request, session, abort
from main import EasyApplyLinkedin
import json
import threading

app =  Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')
	#'<h1>Hello World, {}.</h1>'.format(name)

@app.route('/Applied/', methods=["POST"])
def redirect():
	email = request.form['email']
	name = request.form['name']
	password = request.form['password']
	location = request.form['location']
	keywords = request.form['keywords']
	data = {'email': email, 'password': password, 'keywords': keywords, 'location': location}
	with open('data.json', 'w') as outfile:
		json.dump(data, outfile)
	with open('data.json') as config_file:
		data = json.load(config_file)
	bot = EasyApplyLinkedin(data)
	t1 = threading.Thread(target=bot.apply)
	t1.start()
	return '<h1>Applied for jobs, {}!!!</h1>'.format(name)
	