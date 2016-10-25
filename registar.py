from flask import Flask
from flask import render_template
from flask import request
import csv
import time

with open('names.csv') as csvfile:
    readCSV = csv.DictReader(csvfile, delimiter=',')

    first_names = []
    last_names = []
    companies = []

    for row in readCSV:
        first_names.append(row['first_name'])
        last_names.append(row['last_name'])
        companies.append(row['company'])

app = Flask(__name__)
@app.route('/', methods = ['GET'])
def render_main():
    return render_template("main.html", f_names=first_names, l_names=last_names, companies = companies)

@app.route('/signup', methods = ['POST'])
def new_signup():
    form_data = request.form
    with open('new_signups.csv','a') as new_signups:
        fieldnames = ['date','first_name','last_name','company','email','newsletter']
        writer = csv.DictWriter(new_signups, fieldnames=fieldnames)
        writer.writerow({'date' : (time.strftime("%d/%m/%Y")) ,'first_name' : form_data['first_name'], 'last_name' : form_data['last_name'], 'company' : form_data['company'], 'email' : form_data['email']})
    new_signups.close()
    return render_template("signup_screen.html")


if __name__ == '__main__':
    app.run(debug=True)
