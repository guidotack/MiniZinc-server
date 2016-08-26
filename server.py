import pymzn
import os
from subprocess import Popen, PIPE
from flask import Flask, json, Response
app = Flask(__name__)

folder = 'models' #where the .mzn files are stored
models = []
for file in os.listdir(folder):
	if file.endswith('.mzn'):
		models.append(file)

@app.route('/')
def Allmodels():
	return json.jsonify(result=models)

#inputs models musn't 'output'
@app.route('/model/<string:model>.json')
def Model(model):
	if (model+".mzn" in models):
		def output_line():
			with Popen(["MiniZinc", folder + '/' + model+".mzn", "-a"], stdout=PIPE, bufsize=1, universal_newlines=True) as p: #-a outputs all solutions
				for line in p.stdout:
					markup = ['----------','==========']
					if line.rstrip() not in markup: #each new solution is a new JSON object
						yield str(pymzn.parse_dzn(line)) #use pymzn to turn output into nice JSON objects
		return Response(output_line(),  mimetype='text/json')
	else:
		return json.jsonify(model="no model found")