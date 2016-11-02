from flask import Flask, redirect, url_for, flash, render_template, request
from flask_login import LoginManager, login_required
from werkzeug.utils import secure_filename
import requests
import csv
import time
import os #library for uploading/manipulating files
import sys

app = Flask(__name__)

# login_manager = LoginManager()
# login_manager.init_app(app)
#
# @login_required
# def admin():


# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     # Here we use a class of some kind to represent and validate our
#     # client-side form data. For example, WTForms is a library that will
#     # handle this for us, and we use a custom LoginForm to validate.
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

# how to check whether the names is already on the list?
# loop .join the first_name, last_name & comapny and loop through current list to see if it already exist

# APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/event', methods = ['GET'])
def render_main():

    preload_names('names.csv')

    with open('new_signups.csv','r') as new_signups:
        find_new_attendees = csv.DictReader(new_signups, delimiter=',')
        for row in find_new_attendees:

            if row['date'] == time.strftime("%d/%m/%Y"):
            #    if (row['first_name'],row['last_name'],row['company']) ...
            #    return ','.join(row['first_name'],row['last_name'],row['company'])
                first_names.append(row['first_name'])
                last_names.append(row['last_name'])
                companies.append(row['company'])

    return render_template("main.html", f_names=first_names, l_names=last_names, companies = companies, date = date)


@app.route('/signup', methods = ['POST'])
def new_signup():
    form_data = request.form
    with open('new_signups.csv','a') as new_signups:
        fieldnames = ['date','first_name','last_name','company','email','newsletter']
        writer = csv.DictWriter(new_signups, fieldnames=fieldnames)
        writer.writerow({'date' : (time.strftime("%d/%m/%Y")) ,'first_name' : form_data['first_name'], 'last_name' : form_data['last_name'], 'company' : form_data['company'], 'email' : form_data['email']})

        # TODO: validate response
        requests.post(
            "https://api.mailgun.net/v3/sandbox3e7227e67a8b424891fd4bc2e2126db0.mailgun.org/messages",
            auth=("api", "key-53ed1f7079a97617110a13a0f80b036e"),
            data={"from": "Mailgun Sandbox <postmaster@sandbox3e7227e67a8b424891fd4bc2e2126db0.mailgun.org>",
                  "to": form_data['email'] ,
                  "subject": "Hello %s" % (form_data['first_name']),
                  "html": "Hello again %s" % (form_data['first_name'])})

    return render_template("signup_screen.html")

@app.route('/register', methods = ['POST'])
def generate_register():
    register_data = request.data
    # print request.json
    print register_data
    import pdb; pdb.set_trace()
    return "string"

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




# New route
# Post request
# Accept a list of ids



#
#
# @app.route('/upload')
# def upload():
#     target = os.path.join(APP_ROOT, 'csv/')
#     print target
#
#     for file in requests.files.getlist('file'):
#         print file
#         filename = file.filename
#         destination = '/'.join([target, filename])
#         file.save(destination)
#     return render_template('upload_completed.html')

# @app.route('/email', methods=['POST'])
# def send_simple_message():
#     return requests.post(
#         "https://api.mailgun.net/v3/sandbox3e7227e67a8b424891fd4bc2e2126db0.mailgun.org/messages",
#         auth=("api", "key-53ed1f7079a97617110a13a0f80b036e"),
#         data={"from": "Mailgun Sandbox <postmaster@sandbox3e7227e67a8b424891fd4bc2e2126db0.mailgun.org>",
#               "to": {{ email }},
#               "subject": "Hello {{ person }}",
#               "html": "Congratulations {{ name }}, you just sent an email with Mailgun!  You are truly awesome!  You can see a record of this email in your logs: https://mailgun.com/cp/log .  You can send up to 300 emails/day from this sandbox server.  Next, you should add your own domain so you can send 10,000 emails/month for free."})


if __name__ == '__main__':
    app.run(debug=True)
