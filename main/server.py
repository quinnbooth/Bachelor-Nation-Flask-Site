from flask import Flask, Response, request, jsonify, render_template
import json
import uuid
import re

app = Flask(__name__)

people_list = {
   "1": {
         "name": "Contestant 1",
         "image": "https://s.cafebazaar.ir/images/icons/vsin.t16_funny_photo-698795fc-9630-4f57-b493-394110c9b280_512x512.png?x-img=v1/resize,h_256,w_256,lossless_false/optimize",
         "description": "This person is very cool!"
   },
   "2": {
         "name": "Contestant 2",
         "image": "https://s.cafebazaar.ir/images/icons/vsin.t16_funny_photo-698795fc-9630-4f57-b493-394110c9b280_512x512.png?x-img=v1/resize,h_256,w_256,lossless_false/optimize",
         "description": "This person is very NOT cool!"
   },
   "3": {
         "name": "Contestant 3",
         "image": "https://s.cafebazaar.ir/images/icons/vsin.t16_funny_photo-698795fc-9630-4f57-b493-394110c9b280_512x512.png?x-img=v1/resize,h_256,w_256,lossless_false/optimize",
         "description": "This person is kinda cool!"
   },
   "4": {
         "name": "Contestant 4",
         "image": "https://s.cafebazaar.ir/images/icons/vsin.t16_funny_photo-698795fc-9630-4f57-b493-394110c9b280_512x512.png?x-img=v1/resize,h_256,w_256,lossless_false/optimize",
         "description": "This person is SUPER cool!"
   }
}

learning_pages = {
   "1": {
      "title": "Fantasy Suite",
      "roses": 2,
      "contestants": [1, 2, 3],
      "description": "This is a description of Fantasy Suites."
   },
   "2": {
      "title": "The Engagement",
      "roses": 1,
      "contestants": [1, 4],
      "description": "Now pick somebody."
   }
}

quiz_pages = {

}


#####################      ROUTES      #####################

@app.route('/')
def home():
   return render_template('home.html')   

@app.route('/learn/<page_num>')
def date(page_num):
   global people_list
   global learning_pages

   data = learning_pages[str(page_num)]
   contestants = []
   for person in data["contestants"]:
      contestants.append(people_list[str(person)])

   return render_template('date.html', data=data, contestants=contestants)   

#####################  AJAX FUNCTIONS  #####################



############################################################

if __name__ == '__main__':
   app.run(debug = True)




