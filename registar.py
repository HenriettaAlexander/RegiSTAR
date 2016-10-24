from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
@app.route('/', methods = ['GET'])
def render_temp():
    return render_template("main.html")



# if __name__ == 'main'
app.run(debug=True)
