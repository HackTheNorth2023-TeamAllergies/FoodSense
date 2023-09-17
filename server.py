from flask import Flask, render_template

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', data={'data':'hello'})

if (__name__ == '__main__'):
    app.run(debug = True)