from flask import Flask
from flask import render_template
from flask import request
import csv

with open('names.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')

    # trying to create a dictionary instead of two arrays
    # attendees = {}

    first_names = []
    last_names = []

    for row in readCSV:
        first_name = row[1]
        last_name = row[2]

        first_names.append(first_name)
        last_names.append(last_name)

        # replacing arrays with dictionary
        # attendees.append(first_names)


    # for i in range(len(first_names)-1):
    #     print first_names[i], last_names[i]

app = Flask(__name__)
@app.route('/', methods = ['GET'])
def render_main():
    return render_template("main.html", f_names=first_names, l_names=last_names)

@app.route('/signup', methods = ['POST'])
def render_signup():
    return render_template("signup_screen.html")

@app.route('/signup', methods = ['POST'])
def new_signup():
    form_data = request.form
    form_info = open("new_signups.csv","a")
    form_info.write(form_data['name'] + "," + form_data['email'])

if __name__ == '__main__':
    app.run(debug=True)
