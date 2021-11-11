
from flask import Flask, request, render_template,jsonify


app = Flask(__name__) 

@app.route('/')
def hello_world():
    return render_template('login.html')

if __name__ == '__main__':
    app.debug = True

    app.run()