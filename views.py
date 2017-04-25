from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGOALCHEMY_DATABASE'] = 'sampletsii'
app.config['MONGO_URI'] = 'mongodb://tsii:Qazyhnol9@ds161890.mlab.com:61890/sampletsii'


mongo = PyMongo(app)
diseases = ['Acne', 'AIDS', 'Alopecia Areata', 'Aneurysm', 'Androgenetic Alopecia', 'Angina', 'Asthma', 'Atherosclerosis',
'ADHD', 'ASD', 'Autoimmune Disease', 'Blood clots', 'Brain Fog']

# from . import app, mongo, diseases

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	if request.method == "POST":
		fname = request.form['firstname']
		lname = request.form['lastname']
		age = request.form['age']
		diseases_name = request.form.getlist('disease_name')
		return redirect(url_for('info', firstname=fname, lastname=lname, age=age, diseases_names=diseases_name))
	return render_template('index.html', diseases=diseases)

@app.route('/personalInfo', methods=['GET', 'POST'])
def personalInfo():
	person = request.args.get('samplePerson')
	ageOfPerson = request.args.get('sampleAge')
	city = request.args.get('sampleCity')
	state = request.args.get('sampleState')
	queryResult = mongo.db.testimonial.find({"name" : person})
	
	for sample in queryResult:
		actualTestimonial = sample['testimonial']
		img = sample['image']

	
	return render_template('personalInfo.html', poi=person, age=ageOfPerson, testimonial=actualTestimonial, image=img, city=city, state=state)


@app.route('/info', methods=['GET', 'POST'])
def info():
	diseases_names = request.args.getlist('diseases_names') # includes the list of diseases that the user entered into the index page
	people = mongo.db.people
	disease_dict = {}
	# list_of_queries =[]
	# for disease in diseases_names:
	# 	queryResult = people.find({"health metrics" : {"$all" : disease}})
	# 	list_of_queries.append(queryResult)

	for disease in diseases_names:
		queryResult = people.find({"health metrics" : {"$all" : [disease]}})
		disease_dict[disease] = queryResult



	# for atom in sample:
	# 	print atom['name']
	return render_template('info.html', firstname=request.args.get('firstname'), lastname=request.args.get('lastname'), age=request.args.get('age'), diseases_names=request.args.getlist('diseases_names'), qR=disease_dict)



if __name__ == '__main__':
	app.run(debug=True)