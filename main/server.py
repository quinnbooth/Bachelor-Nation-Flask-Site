from flask import Flask, Response, request, jsonify, render_template
import json
import uuid
import re

app = Flask(__name__)

people_list = {
   "1": {
         "name": "Kelsey A.",
         "image": "https://heavy.com/wp-content/uploads/2024/02/kelsey-anderson-bachelor.jpg?quality=65&strip=all",
         "description": "This person is very cool!"
   },
   "2": {
         "name": "Daisy",
         "image": "https://hips.hearstapps.com/hmg-prod/images/daisy-bio-170217-4395-65ae8e5560c64.jpg?crop=1xw:0.53525xh;center,top&resize=1200:*",
         "description": "This person is very NOT cool!"
   },
   "3": {
         "name": "Rachel",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362682/e8cffaf4f8b6993e976bac6267b01e48/320x180-Q90_e8cffaf4f8b6993e976bac6267b01e48.jpg",
         "description": "This person is kinda cool!"
   },
   "4": {
         "name": "Maria",
         "image": "https://wegotthiscovered.com/wp-content/uploads/2024/01/The-Bachelorette_-Maria.png",
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
      "nextPage": "/rose/1" # should lead to bracket  
   },
   "3": {
      "text":  '''   Welcome to the First Week, specifically the First Night!
                     Tonight, each woman will make their “limousine entrance” and meet Joey for the first time.
                     Then, a cocktail party inside the Bachelor Mansion will give the women a chance to talk to Joey 1-on-1. Before the night is over, Joey will have his first rose ceremony of the season.)
               ''',
      "textMedia": "",
      "speakerImage": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRX7RRbcZWghn-ZIql1Q8wv-IZXzAwOBahfyT6oRmkJJg&s",
      "speakerName": "Jesse Palmer",
      "audio": "implement this last if we have time???",
      "nextPage": "/rose/2"
   },
   "4": {
      "text":  '''   The first week is over!
                     The next ~7 weeks/episodes will be group dates and 1-on-1’s galore! 
                     We’ll always end each night with a rose ceremony of course. We’ll even be traveling the world for these dates! 
                     And finally, we’ll get down to 4 contestants and get ready for hometowns.
               ''',
      "textMedia": "",
      "speakerImage": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRX7RRbcZWghn-ZIql1Q8wv-IZXzAwOBahfyT6oRmkJJg&s",
      "speakerName": "Jesse Palmer",
      "audio": "implement this last if we have time???",
      "nextPage": "/rose/3"
   }
}

rose_pages = {
   "1": {
      "title": "Bracket",
      "roses": 2,
      "contestants": [1, 2, 3],
      "description": "This is a description of Fantasy Suites. Hover over people for a description. Then give out your roses one by one.",
      "nextPage": "/learn/3",
      "handbook": "TBD"
   },
   "2": {
      "title": "Limo Entrances",
      "roses": 5,
      "contestants": [1, 4, 3, 2, 3, 1, 4, 2],
      "description": "This is a description of TEST. Hover over people for a description. Then give out your roses one by one. ",
      "nextPage": "/learn/4", 
      "handbook": "Limousine Entrances are when the contestants meet Joey for the first time! Each woman gets to exit the limo (or whichever vessel they choose) and meet Joey one-on-one, usually introducing herself with a prop that’s significant to her, or her background. It’s important to make a good and lasting impression!"
   },
   "3": {
      "title": "Hometowns",
      "roses": 3,
      "contestants": [1, 2, 3, 4],
      "description": "This is a description of TEST. Hover over people for a description. Then give out your roses one by one. ",
      "nextPage": "/rose/4",
      "handbook": "What are hometown visits? Why are they relevant? Hometown visits are when the bachelor visits the hometown of each of the remaining 4 contestants and meets their families. This is a chance to see how well he blinds with the contestants’ families and for his bond with each contestant to get deeper and stronger. After all the hometown visits, Joey will eliminate 1 of the women in the rose ceremony, so stakes are high!"
   },
   "4": {
      "title": "Fantasy Suites",
      "roses": 2,
      "contestants": [1, 2, 3],
      "description": "This is a description of TEST. Hover over people for a description. Then give out your roses one by one. ",
      "nextPage": "/rose/5",
      "handbook": "What are Fantasy Suites? The Fantasy Suites phase occurs toward the end of each season and takes place in a luxurious setting like a hotel suite or private accommodation. During this stage, the bachelor and the three remaining contestants are given the opportunity to spend private, overnight 1-on-1 dates together without cameras present - a great opportunity for them to deepen their conversations and connections, and discuss more personal matters before the next rose ceremony!"
   },
   "5": {
      "title": "Engagement",
      "roses": 1,
      "contestants": [1, 2],
      "description": "This is a description of TEST. Hover over people for a description. Then give out your roses one by one. ",
      "nextPage": "/quiz",
      "handbook": "What happens in the engagement ceremony? During the engagement ceremony, Joey chooses which contestant he will marry, and which he will reject. Each one of the girls will arrive to the engagement spot in an order they don’t know. The first woman is usually the woman that gets broken up with, and the last woman is the one that Joey proposes to. Note: The bachelor doesn’t necessarily need to propose to someone or leave the show with them!"
   }
}

quiz_pages = {
   "1": {
      "questionId": "1",
      "question": "In a 2-on-1, what usually happens with the girl that doesn’t get the rose?",
      "questionType": "mult_choice",
      "choices": ["She goes back to the mansion and waits for the next events",
                  "She joins the group date that Joey goes on next ",
                  "She is sent home, but first she gets to say her goodbyes to the girls",
                  "She is sent home immediately"],
      "answer": [3]
   },
   "2": {
      "questionId": "2",
      "question": "Question here?",
      "questionType": "fill_blank",
      "choices": [],
      "answer": ["answer here"]
   },
   "3": {
      "questionId": "3",
      "question": "Question here?",
      "questionType": "true_false",
      "choices": [],
      "answer": ["true"]
   },
   "4": {
      "questionId": "4",
      "question": "Question here?",
      "questionType": "true_false",
      "choices": [],
      "answer": ["true"]
   },
   "5": {
      "questionId": "5",
      "question": "Question here?",
      "questionType": "mult_select",
      "choices": ["blah",
                  "blah",
                  "blah",
                  "blah"],
      "answer": [0, 2, 3]
   },
   "6": {
      "questionId": "6",
      "question": "Question here?",
      "questionType": "sort",
      "choices": ["blah",
                  "blah",
                  "blah",
                  "blah"],
      "answer": [0, 1, 2, 3, 4]
   }
}

# Sets used to keep track of which questions user got correct / incorrect in quiz section
correct = list()
incorrect = list()


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

@app.route('/quiz')
def quiz_home():
   global correct
   global incorrect
   data = {
      "correct": correct,
      "incorrect": incorrect
   }
   return render_template('quiz_home.html', data=data)

@app.route('/quiz/<page_num>')
def quiz(page_num):
   global quiz_pages
   data = quiz_pages[str(page_num)]
   return render_template('quiz.html', data=data)   

#####################  AJAX FUNCTIONS  #####################

@app.route('/quiz_handler', methods=['POST'])
def search():
   global correct
   global incorrect
   json_data = request.get_json()
   isCorrect = json_data["isCorrect"]
   question_id = json_data["id"]
   
   if isCorrect:
      correct.append(question_id)
   else:
      incorrect.append(question_id)
            
   return jsonify({'redirect': '/quiz'})

############################################################

if __name__ == '__main__':
   app.run(debug = True)




