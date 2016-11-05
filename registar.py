from flask import Flask, redirect, url_for, flash, render_template, request
from flask_login import LoginManager, login_required
from werkzeug.utils import secure_filename
from wtforms import Form, BooleanField, StringField, validators
import requests
import csv
import time
import os #library for uploading/manipulating files
import sys

app = Flask(__name__)

# login_manager = LoginManager()
# login_manager.init_app(app)
#
#
# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)
#
# class RegistrationForm(Form):
#     username     = StringField('Username', [validators.Length(min=4, max=25)])
#     email        = StringField('Email Address', [validators.Length(min=6, max=35)])
#     accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])
#
# @app.route('/login', methods=['GET', 'POST'])
# def login(request):
#     form = RegistrationForm(request.POST)
#     if request.method == 'POST' and form.validate():
#         user = User()
#         user.username = form.username.data
#         user.email = form.email.data
#         user.save()
#         redirect('logged-in')
#     return render_response('logged-in', form=form)
#
#     form = LoginForm()
#     if form.validate_on_submit():
#         # Login and validate the user.
#         # user should be an instance of your `User` class
#         login_user(user)
#
#         flask.flash('Logged in successfully.')
#
#         next = flask.request.args.get('next')
#         # next_is_valid should check if the user has valid
#         # permission to access the `next` url
#         if not next_is_valid(next):
#             return flask.abort(400)
#
#         return flask.redirect(next or flask.url_for('index'))
#     return flask.render_template('login.html', form=form)

first_names = []
last_names = []
companies = []
date = time.strftime("%d/%m/%Y")


def preload_names(csv_file_name):
    with open(csv_file_name) as csvfile:
        readCSV = csv.DictReader(csvfile, delimiter=',')
        for row in readCSV:
            first_names.append(row['first_name'])
            last_names.append(row['last_name'])
            companies.append(row['company'])

preload_names('names.csv')


@app.route('/event', methods = ['GET'])
def render_main():
    not_on_the_list = []
    with open('new_signups.csv','r') as new_signups:
        find_new_attendees = csv.DictReader(new_signups, delimiter=',')
        for row in find_new_attendees:
            if row['date'] == time.strftime("%d/%m/%Y"):
                for i in range(len(first_names)):
                    if "".join([row['first_name'],row['last_name'],row['company']]) != "".join([first_names[i],last_names[i],companies[i]]):
                        not_on_the_list.append('y')
                if len(not_on_the_list) == len(first_names):
                    with open('new_signups.csv','r') as new_signups:
                        find_new_attendees = csv.DictReader(new_signups, delimiter=',')
                        for row in find_new_attendees:
                            first_names.append(row['first_name'])
                            last_names.append(row['last_name'])
                            companies.append(row['company'])
                print len(not_on_the_list), len(first_names), len(not_on_the_list) == len(first_names)

    return render_template("main.html", f_names=first_names, l_names=last_names, companies = companies, date = date)



@app.route('/signup', methods = ['POST'])
def new_signup():
    form_data = request.form
    with open('new_signups.csv','a') as new_signups:
        fieldnames = ['date','first_name','last_name','company','email','newsletter']
        writer = csv.DictWriter(new_signups, fieldnames=fieldnames)
        writer.writerow({'date' : (time.strftime("%d/%m/%Y")) ,'first_name' : form_data['first_name'], 'last_name' : form_data['last_name'], 'company' : form_data['company'], 'email' : form_data['email'], 'newsletter' : form_data['newsletter']})

        # print len(not_on_the_list), len(first_names), len(not_on_the_list) == len(first_names)
        # if len(not_on_the_list) == len(first_names):
        #     with open('new_signups.csv','r') as new_signups:
        #         find_new_attendees = csv.DictReader(new_signups, delimiter=',')
        #         for row in find_new_attendees:
        #             first_names.append(row['first_name'])
        #             last_names.append(row['last_name'])
        #             companies.append(row['company'])

        # TODO: validate response
        requests.post(
            "https://api.mailgun.net/v3/sandbox3e7227e67a8b424891fd4bc2e2126db0.mailgun.org/messages",
            auth=("api", "key-53ed1f7079a97617110a13a0f80b036e"),
            data={"from": "Mailgun Sandbox <postmaster@sandbox3e7227e67a8b424891fd4bc2e2126db0.mailgun.org>",
                  "to": form_data['email'] ,
                  "subject": "Welcome to Registar %s!" % (form_data['first_name']),
                  "html": "Hi %s Thank you for signing up for this event with registar. We hope you've had a great time and we're looking forward to seeing you soon at one of our events." % (form_data['first_name'])})

    return render_template("signup_screen.html")

# @app.route('/register', methods = ['POST'])
# def generate_register():
#     register_data = request.data
#     # print request.json
#     print register_data
#     import pdb; pdb.set_trace()
#     return "string"
#
@app.route('/')
def signin():
    return render_template("homepage.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] == 'csv'


@app.route('/admin', methods = ['GET','POST'] )
def upload():
    print 0
    if request.method == 'POST':
        # check if the post request has the file part
        print 1
        print request.files
        if 'upload-file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['upload-file']
        # if user does not select file, browser also
        # submit a empty part without filename
        print 2
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        print file
        print allowed_file(file.filename)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print filename
            # file.save(os.path.join('/tmp', filename))
            file.save(os.path.join(app.root_path,'registers', secure_filename(request.form['event_name']))+'.csv')

            return redirect(url_for('signin'))
    else:
        return render_template('admin_view.html')


if __name__ == '__main__':
    app.run(debug=True)
