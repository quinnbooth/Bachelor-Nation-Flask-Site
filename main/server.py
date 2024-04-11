from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
app = Flask(__name__)
import json
import uuid
import re

#####################      ROUTES      #####################

@app.route('/')
def welcome():
   return render_template('welcome.html')   


#####################  AJAX FUNCTIONS  #####################



############################################################

if __name__ == '__main__':
   app.run(debug = True)




