from flask import Flask, flash, redirect, render_template, request, session, abort

app =  Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')
	#'<h1>Hello World, {}.</h1>'.format(name)

@app.route('/<name>/')
def redirect(name):
	return '<h1>Applied for jobs, {}!!!.</h1>'.format(name)