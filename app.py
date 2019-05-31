import os
from flask import Flask, render_template, request
import TestCVInfo
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

final_output = TestCVInfo.generate_output()



@app.route("/")

def index():
	return render_template("UserInfo.html")







@app.route("/getRequirements",methods = ['POST'])

def requirements():
	
	languages = request.form['progLang']
	platforms = request.form['platforms']
	tools = request.form['tools']
	
	fp = open('requirements.txt', 'w')
	fp.seek(0)
	fp.truncate()

	fp.write(languages + "\n")
	fp.write(platforms + "\n")
	fp.write(tools + "\n")
	fp.close()
	
	
	return render_template("complete.html")


@app.route("/uploadDetails", methods = ['POST'])

def upload():	
	firstName = request.form['firstName']
	lastName = request.form['lastName']
	email = request.form['email']
	contact = request.form['contact']
	experience = request.form['experience']
	location = request.form['location']
	fp = open('userDetails.txt' , 'a')
	fp.write(firstName)
	fp.write(',')
	fp.write(lastName)
	fp.write(',')
	fp.write(email)
	fp.write(',')
	fp.write(contact)
	fp.write(',')
	fp.write(experience)
	fp.write(',')
	fp.write(location)
	fp.write(',')

	temp = {
		"naav" : firstName,
		"adnav" : lastName,
		"email" : email
	}
	target = os.path.join(APP_ROOT, 'fileUploads/')

	if not os.path.isdir(target):
		os.mkdir(target)
	
	tempFile = request.files.getlist("file")
	for file in tempFile:

		filename = file.filename
		destination = "/".join([target,filename])

		file.save(destination)

	fp.write(filename)
	fp.write("\n")
	fp.close()
	return render_template("complete.html")



@app.route('/table')
def table():

	record = []

	for person in final_output:
		person_details = person.split(',')
		tempJsonObject = {

			"name" : person_details[0] + person_details[1],
			"email" : person_details[2],
			"contact" : person_details[3],
			"experience" : person_details[4],
			"location" : person_details[5],
			"resume" : person_details[6]
			
		}

		record.append(tempJsonObject)
	return render_template('tables.html', result = record)



if __name__ == "__main__": 
	app.run(port = 4555, debug = True)
