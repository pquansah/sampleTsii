from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo
from forms import ApplicantForm, LoginForm


app = Flask(__name__)

app.config['MONGOALCHEMY_DATABASE'] = 'sampletsii'
app.config['MONGO_URI'] = 'mongodb://tsii:Qazyhnol9@ds161890.mlab.com:61890/sampletsii'
app.config['SECRET_KEY'] = '435897348y348f3784hf7'

mongo = PyMongo(app)
diseases = ['Acne', 'AIDS', 'Alopecia Areata', 'Aneurysm', 'Androgenetic Alopecia', 'Angina', 'Asthma', 'Atherosclerosis',
'ADHD', 'ASD', 'Autoimmune Disease', 'Blood clots', 'Brain Fog']


@app.route('/login', methods=['GET', 'POST'])
def login():
	login_form = LoginForm()
	if request.method == "POST":
		email = login_form.email.data
		password = login_form.password.data
		person = mongo.db.people.find({"email" : email})
		for sample in person:
			diseases = sample['health metrics']
			firstname = sample['fname']
			lastname = sample['lname']
			age = sample['age']

		return redirect(url_for('info', firstname=firstname, lastname=lastname, age=age, diseases_names=diseases))

	return render_template('login.html', login_form=login_form)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
	return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def index():
	applicant_form = ApplicantForm()
	if applicant_form.validate_on_submit():
		fname = applicant_form.fname.data
		lname = applicant_form.lname.data
		age = applicant_form.age.data
		phone_number = applicant_form.phone_number.data
		email = applicant_form.email.data
		city = applicant_form.city.data
		state = applicant_form.state.data
		zip_code = applicant_form.zip_code.data
		password = applicant_form.password.data


		diseases_name = request.form.getlist('disease_name')
		mongo.db.people.insert({"fname" : fname, "lname" : lname, "email" : email, "phone number" : phone_number, "city" : city, "state" : state, "zip" : zip_code, "age" : age, "health metrics" : diseases_name, "password" : password})
		return redirect(url_for('info', firstname=fname, lastname=lname, age=age, diseases_names=diseases_name))

	return render_template('login1.html', applicant_form=applicant_form, diseases=diseases)


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