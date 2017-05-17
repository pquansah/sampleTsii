from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo
from forms import ApplicantForm, LoginForm, EditForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap


# initializes app for Flask
app = Flask(__name__)

# initializes Bootstrap for app, frontend purposes
Bootstrap(app)

# MongoDB Database name sampletsii and initialization
app.config['MONGOALCHEMY_DATABASE'] = 'sampletsii'
app.config['MONGO_URI'] = 'mongodb://tsii:Qazyhnol9@ds161890.mlab.com:61890/sampletsii'
app.config['SECRET_KEY'] = '435897348y348f3784hf7'


# initialize database for app using mongoDB
mongo = PyMongo(app)

# list of diseases (temporary, will go in database soon)
diseases = ['Acne', 'AIDS', 'Alopecia Areata', 'Aneurysm', 'Androgenetic Alopecia', 'Angina', 'Asthma', 'Atherosclerosis',
'ADHD', 'ASD', 'Autoimmune Disease', 'Blood clots', 'Brain Fog']


# edit page, where user can edit information that he or she wants to about him or herself
@app.route('/edit', methods=['GET', 'POST'])
def edit():
	edit_form = EditForm()
	message = None

	# perfoming updates on user if he or she gives information
	if edit_form.validate_on_submit():
		name = edit_form.name.data
		age = edit_form.age.data
		phone_number = edit_form.phone_number.data
		email = edit_form.email.data
		city = edit_form.city.data
		state = edit_form.state.data
		zip_code = edit_form.zip_code.data

		firstname = request.args.get('firstname')
		lastname = request.args.get('lastname')

		person = mongo.db.people.find({"fname" : firstname})

		# perfoms updates on fields that have been given information
		for sample in person:
			if name != "":
				name_list = name.split(" ")
				mongo.db.people.update({"fname" : firstname}, {"$set" : {"fname" : name_list[0]}})
				mongo.db.people.update({"fname" : firstname}, {"$set" : {"lname" : name_list[1]}})
				mongo.db.people.update({"fname" : firstname}, {"$set" : {"name" : name}})
				firstname = name_list[0]
				lastname = name_list[1]

			if age != "":
				mongo.db.people.update({"fname" : firstname}, {"$set" : {"age" : age}})
			if phone_number != "":
				mongo.db.people.update({"fname" : firstname}, {"$set" : {"phone number" : phone_number}})
			if email != "":
				mongo.db.people.update({"fname" : firstname}, {"$set" : {"email" : email}})
			if city != "":
				mongo.db.people.update({"fname" : firstname}, {"$set" : {"city" : city}})
			if state != "":
				mongo.db.people.update({"fname" : firstname}, {"$set" : {"state" : state}})
			if zip_code != "":
				mongo.db.people.update({"fname" : firstname}, {"$set" : {"zip" : zip_code}})

		message = 'Edits successfully submitted'


	return render_template('edit.html', edit_form=edit_form, diseases=request.args.getlist('diseases_names'), message=message)

# login page, user will need to provide a email and password to login the pages
@app.route('/login', methods=['GET', 'POST'])
def login():
	# login form with email and password field
	login_form = LoginForm()
	message = None
	if login_form.validate_on_submit():

		# if login successfully submits with no errors, pull the email and password and check against database
		email = login_form.email.data
		password = login_form.password.data
		person = mongo.db.people.find({"email" : email})

		# this for loop is to retrieve information from the person so it can be used for display on their profile
		for sample in person:
			diseases = sample['health metrics']
			firstname = sample['fname']
			lastname = sample['lname']
			age = sample['age']
			real_password = sample['password']

		if check_password_hash(real_password, password):
			# return redirect(url_for('info', firstname=firstname, lastname=lastname, age=age, diseases_names=diseases))
			return redirect(url_for('user', firstname=firstname, lastname=lastname, age=age, diseases_names=diseases))
		else:
			message = 'Invalid Username or Password'

	return render_template('login.html', login_form=login_form, message=message)

# home page, user can either login or signup
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
	return render_template('home.html')

# signup page, in order for the user to have a successful signup, they would need to provide input for all fields
@app.route('/signup', methods=['GET', 'POST'])
def index():
	applicant_form = ApplicantForm()

	# if the form is successfully processed, meaning all fields are filled out, we will add the user to the database
	if applicant_form.validate_on_submit():
		fname = applicant_form.fname.data
		lname = applicant_form.lname.data
		age = applicant_form.age.data
		phone_number = applicant_form.phone_number.data
		email = applicant_form.email.data
		city = applicant_form.city.data
		state = applicant_form.state.data
		zip_code = applicant_form.zip_code.data
		password = generate_password_hash(applicant_form.password.data, method='sha256')


		diseases_name = request.form.getlist('disease_name')
		mongo.db.people.insert({"fname" : fname, "lname" : lname, "email" : email, "phone number" : phone_number, "city" : city, "state" : state, "zip" : zip_code, "age" : age, "health metrics" : diseases_name, "password" : password})
		return redirect(url_for('info', firstname=fname, lastname=lname, age=age, diseases_names=diseases_name))

	return render_template('signup.html', applicant_form=applicant_form, diseases=diseases)

# user can look at basic information of other users that have similar symptons as they do
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


# information page for user, so they will be able to see every user from the database that have similar symptons as they do
@app.route('/info', methods=['GET', 'POST'])
def info():
	diseases_names = request.args.getlist('diseases_names') # includes the list of diseases that the user entered into the index page
	people = mongo.db.people
	disease_dict = {}

	for disease in diseases_names:
		queryResult = people.find({"health metrics" : {"$all" : [disease]}})
		disease_dict[disease] = queryResult


	return render_template('info.html', firstname=request.args.get('firstname'), lastname=request.args.get('lastname'), age=request.args.get('age'), diseases_names=request.args.getlist('diseases_names'), qR=disease_dict)

# page user sees when he or she successfully logs in or signs up
@app.route('/user', methods=['GET', 'POST'])
def user():
	firstname = request.args.get('firstname')
	lastname = request.args.get('lastname')
	diseases_names = request.args.getlist('diseases_names')
	age_of_person = request.args.get('age')

	return render_template('user.html', fname=firstname, lname=lastname, age=age_of_person, diseases=diseases_names)

if __name__ == '__main__':
	app.run(debug=True)