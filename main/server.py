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

learn_pages = {
   "1": {
      "text":  '''   Welcome to The Bachelor!\n
                     I’m your host Jesse Palmer, and in this show, we will help our Bachelor, Joey, find (and possibly marry) his true love over the course of 11 weeks!\n
                     For this, we have selected 32 lucky girls who Joey will have the opportunity to interact with, and choose among as the weeks go by until we are left with 2 special finalists!\n
                     Let’s go ahead and start!
               ''',
      "textMedia": "",
      "speakerImage": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRX7RRbcZWghn-ZIql1Q8wv-IZXzAwOBahfyT6oRmkJJg&s",
      "speakerName": "Jesse Palmer",
      "audio": "implement this last if we have time???",
      "nextPage": "/learn/2"
   },
   "2": {
      "text":  '''   Hey there! I'm Joey, a 28-year-old tennis coach living the dream in Hawaii. A couple of things about me:\n\n
                     * Big fan of keeping things chill—drama isn't my game.\n
                     * I'm all about kindness and positive vibes.\n
                     * My biggest fear? Choosing someone who wouldn't choose me back.\n
                     * Sometimes I feel the pressure to be perfect, but I'm working on embracing the imperfections.\n
                     * I'm on the lookout for that soulmate connection, hoping to find my forever partner.
               ''',
      "textMedia": "",
      "speakerImage": "https://cdn.vox-cdn.com/thumbor/1NO2SkFoypW9pVXBSzGrADH8Iq8=/1400x1400/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/25213676/BachelorJoey_ABC.jpg",
      "speakerName": "Joey",
      "audio": "implement this last if we have time???",
      "nextPage": "/rose/1"
   },
   "3": {
      "text":  '''   TEST :)
               ''',
      "textMedia": "",
      "speakerImage": "https://cdn.vox-cdn.com/thumbor/1NO2SkFoypW9pVXBSzGrADH8Iq8=/1400x1400/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/25213676/BachelorJoey_ABC.jpg",
      "speakerName": "Joey",
      "audio": "implement this last if we have time???",
      "nextPage": "/rose/2"
   }
}

rose_pages = {
   "1": {
      "title": "Fantasy Suite",
      "roses": 2,
      "contestants": [1, 2, 3],
      "description": "This is a description of Fantasy Suites. Hover over people for a description. Then give out your roses one by one.",
      "nextPage": "/learn/3"
   },
   "2": {
      "title": "TEST",
      "roses": 5,
      "contestants": [1, 4, 3, 2, 3, 1, 4, 2],
      "description": "This is a description of TEST. Hover over people for a description. Then give out your roses one by one. ",
      "nextPage": "/"
   }
}

quiz_pages = {

}


#####################      ROUTES      #####################

@app.route('/')
def home():
   return render_template('home.html')   

@app.route('/rose/<page_num>')
def rose(page_num):
   global people_list
   global rose_pages
   data = rose_pages[str(page_num)]
   contestants = []
   for person in data["contestants"]:
      contestants.append(people_list[str(person)])
   return render_template('rose.html', data=data, contestants=contestants)

@app.route('/learn/<page_num>')
def learn(page_num):
   global learn_pages
   data = learn_pages[str(page_num)]
   return render_template('learn.html', data=data)   

#####################  AJAX FUNCTIONS  #####################



############################################################

if __name__ == '__main__':
   app.run(debug = True)




