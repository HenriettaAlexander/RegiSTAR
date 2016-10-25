from flask import Flask
from flask import render_template
from flask import request
import csv
import time

# if the first_names are the same, the first one will be found and the last_name for it will be returned (incorrect)
first_names = []
last_names = []
companies = []
date = time.strftime("%d/%m/%Y")


with open('names.csv') as csvfile:
    readCSV = csv.DictReader(csvfile, delimiter=',')
    for row in readCSV:
        first_names.append(row['first_name'])
        last_names.append(row['last_name'])
        companies.append(row['company'])



# how to check whether the names is already on the list?
# loop .join the first_name, last_name & comapny and loop through current list to see if it already exist
app = Flask(__name__)
@app.route('/', methods = ['GET'])
def render_main():
    with open('new_signups.csv','r') as new_signups:
        find_new_attendees = csv.DictReader(new_signups, delimiter=',')
        for row in find_new_attendees:
            if row['date'] == time.strftime("%d/%m/%Y"):
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

    return render_template("signup_screen.html")


if __name__ == '__main__':
    app.run(debug=True)
