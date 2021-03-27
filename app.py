from flask import Flask, flash, redirect, render_template, request, session, abort

app =  Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')
	#'<h1>Hello World, {}.</h1>'.format(name)

@app.route('/Applied/', methods=["POST"])
def redirect():
	name = request.form['name']
	return '<h1>Applied for jobs, {}!!!</h1>'.format(name)