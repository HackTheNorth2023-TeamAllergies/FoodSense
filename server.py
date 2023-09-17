from flask import Flask, render_template, request
from detect import vision

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', data={'data':'hello'})

@app.route('/picture', methods=['POST'])
def sendVision():
    vision(request.img)

if (__name__ == '__main__'):
    app.run(debug = True)