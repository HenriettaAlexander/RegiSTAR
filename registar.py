from flask import Flask
from flask import render_template
from flask import request
import csv

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
def render_signup():
    return render_template("signup_screen.html")


# get this function to write to existent excel file so that new person is included on the list
@app.route('/signup', methods = ['POST'])
def new_signup():
    form_data = request.form
    fields = ["first", "second", "third"]
    with open('new_signups.csv') as csvfile:
        form_info = open("new_signups.csv","a")
        form_info.write(form_data['name'] + "," + form_data['email'])
        form_info = close("new_signups.csv")

if __name__ == '__main__':
    app.run(debug=True)
