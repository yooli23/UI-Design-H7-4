from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
app = Flask(__name__)


# ROUTES
@app.route('/')
def home():
   return render_template('home.html')   

@app.route('/learn')
def learn():
   return render_template('learn.html')   

@app.route('/test')
def test():
   return render_template('test.html')   



if __name__ == '__main__':
   app.run(debug = True)




