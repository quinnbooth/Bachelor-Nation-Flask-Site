from flask import Flask, Response, request, jsonify, render_template
import json
import uuid
import re

app = Flask(__name__)

main_images = {
   "host": "https://scontent-lga3-1.xx.fbcdn.net/v/t1.6435-9/163580111_288668689295431_2707202046743395725_n.jpg?_nc_cat=110&ccb=1-7&_nc_sid=5f2048&_nc_ohc=62bwzzbew-UAb6pIuaB&_nc_ht=scontent-lga3-1.xx&oh=00_AfCPkt3xUkIo7M5b7m4rBqlHmvYQHG2YFmYEFub----_9w&oe=66456A48",
   "bachelor": "https://cdn.vox-cdn.com/thumbor/1NO2SkFoypW9pVXBSzGrADH8Iq8=/1400x1400/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/25213676/BachelorJoey_ABC.jpg"
}

# rn, all the same vids for testing
main_vids = {
   "hometowns": {
      "Kelsey A.": "https://www.youtube.com/embed/cpak2-HWohw?si=CdAe7kLk7kSOPHiI&amp;start=106",
      "Rachel": "https://www.youtube.com/embed/cpak2-HWohw?si=CdAe7kLk7kSOPHiI&amp;start=106",
      "Maria": "https://www.youtube.com/embed/cpak2-HWohw?si=CdAe7kLk7kSOPHiI&amp;start=106",
      "Daisy": "https://www.youtube.com/embed/cpak2-HWohw?si=CdAe7kLk7kSOPHiI&amp;start=106"
   },
   "fantasy_suites": {
      "Kelsey A.": "https://www.youtube.com/embed/cpak2-HWohw?si=CdAe7kLk7kSOPHiI&amp;start=106",
      "Rachel": "https://www.youtube.com/embed/cpak2-HWohw?si=CdAe7kLk7kSOPHiI&amp;start=106",
      "Daisy": "https://www.youtube.com/embed/cpak2-HWohw?si=CdAe7kLk7kSOPHiI&amp;start=106"
   },
   "engagement": {
      "Kelsey A.": "https://www.youtube.com/embed/cpak2-HWohw?si=CdAe7kLk7kSOPHiI&amp;start=106",
      "Daisy": "https://www.youtube.com/embed/cpak2-HWohw?si=CdAe7kLk7kSOPHiI&amp;start=106"
   }
}

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
   },
   "5": {
         "name": "Allison",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362397/0fa781b5411ff6127e806dedf6e1404b/1000x400-Q90_0fa781b5411ff6127e806dedf6e1404b.jpg",
         "description": "This person is SUPER cool!"
   },
   "6": {
         "name": "Autumn",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362398/9e3f9d1ccc324feef9ecdac4f6442995/1000x400-Q90_9e3f9d1ccc324feef9ecdac4f6442995.jpg",
         "description": "This person is SUPER cool!"
   },
   "7": {
         "name": "Chandler",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362399/63f493f17ef609dcd15a4a2f6d698551/166x166-Q90_63f493f17ef609dcd15a4a2f6d698551.jpg",
         "description": "This person is SUPER cool!"
   },
   "8": {
         "name": "Chrissa",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362404/c6085134bf425c566d33eba2e1e6b36e/166x166-Q90_c6085134bf425c566d33eba2e1e6b36e.jpg",
         "description": "This person is SUPER cool!"
   },
   "9": {
         "name": "Edwina",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362410/cdd1fa5318d92221329b5f4b9a0fa6b7/166x166-Q90_cdd1fa5318d92221329b5f4b9a0fa6b7.jpg",
         "description": "This person is SUPER cool!"
   },
   "10": {
         "name": "Erika",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362411/b6eba7c304b944a540ea5e1279b6a077/166x166-Q90_b6eba7c304b944a540ea5e1279b6a077.jpg",
         "description": "This person is SUPER cool!"
   },
   "11": {
         "name": "Evalin",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362486/15a41c1653147a5a9dbb1aa8b30b5a16/166x166-Q90_15a41c1653147a5a9dbb1aa8b30b5a16.jpg",
         "description": "This person is SUPER cool!"
   },
   "12": {
         "name": "Jenn",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362491/6f3352fede1dbd6b6f1634c554871f3b/166x166-Q90_6f3352fede1dbd6b6f1634c554871f3b.jpg",
         "description": "This person is SUPER cool!"
   },
   "13": {
         "name": "Jess",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362515/bdda79724754e41d1edb66e86b292196/166x166-Q90_bdda79724754e41d1edb66e86b292196.jpg",
         "description": "This person is SUPER cool!"
   },
   "14": {
         "name": "Katelyn",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362576/14a66c5c15561525eb359088e53eac8c/166x166-Q90_14a66c5c15561525eb359088e53eac8c.jpg",
         "description": "This person is SUPER cool!"
   },
   "15": {
         "name": "Kayla",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362582/cc97aaeddc7e86cf64bc82b524b51478/166x166-Q90_cc97aaeddc7e86cf64bc82b524b51478.jpg",
         "description": "This person is SUPER cool!"
   },
   "16": {
         "name": "Kelsey T.",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362600/724db8e0fda6a13e5699f7cc968bb780/166x166-Q90_724db8e0fda6a13e5699f7cc968bb780.jpg",
         "description": "This person is SUPER cool!"
   },
   "17": {
         "name": "Kyra",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362608/bbd18769e19f61942a398734da3a5d98/166x166-Q90_bbd18769e19f61942a398734da3a5d98.jpg",
         "description": "This person is SUPER cool!"
   },
   "18": {
         "name": "Lanie",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362614/3c08f4afcb9e2816e8d80bcd8f33241d/166x166-Q90_3c08f4afcb9e2816e8d80bcd8f33241d.jpg",
         "description": "This person is SUPER cool!"
   },
   "19": {
         "name": "Lauren",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362618/ea9437fad00456c0f8bcf6802d12f9da/166x166-Q90_ea9437fad00456c0f8bcf6802d12f9da.jpg",
         "description": "This person is SUPER cool!"
   },
   "20": {
         "name": "Lea",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362622/2facb01d9e9bbc8f475308c5c3933e58/166x166-Q90_2facb01d9e9bbc8f475308c5c3933e58.jpg",
         "description": "This person is SUPER cool!"
   },
   "21": {
         "name": "Lexi",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362628/b8df1b8af1b7dc1615b1ff10bcdf7b29/166x166-Q90_b8df1b8af1b7dc1615b1ff10bcdf7b29.jpg",
         "description": "This person is SUPER cool!"
   },
   "22": {
         "name": "Madina",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362636/5e195207dc93bf388757cce280fd0e38/166x166-Q90_5e195207dc93bf388757cce280fd0e38.jpg",
         "description": "This person is SUPER cool!"
   },
   "23": {
         "name": "Marlena",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362659/e757fdeef9bebce993839a0a7c5660c8/166x166-Q90_e757fdeef9bebce993839a0a7c5660c8.jpg",
         "description": "This person is SUPER cool!"
   },
   "24": {
         "name": "Nat",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362674/2a5fe05c901758aee25019a2992e2267/166x166-Q90_2a5fe05c901758aee25019a2992e2267.jpg",
         "description": "This person is SUPER cool!"
   },
   "25": {
         "name": "Sam",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362694/79584baa688bac89bdda0cc67c09eebe/166x166-Q90_79584baa688bac89bdda0cc67c09eebe.jpg",
         "description": "This person is SUPER cool!"
   },
   "26": {
         "name": "Samantha",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362702/5b690e89d3803d2731d659f7aec0b062/166x166-Q90_5b690e89d3803d2731d659f7aec0b062.jpg",
         "description": "This person is SUPER cool!"
   },
   "27": {
         "name": "Sandra",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362776/52852754a54ae540d8cbc2cef9e1760e/166x166-Q90_52852754a54ae540d8cbc2cef9e1760e.jpg",
         "description": "This person is SUPER cool!"
   },
   "28": {
         "name": "Starr",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362782/449fa9825f124fbc031a39c0d581f311/166x166-Q90_449fa9825f124fbc031a39c0d581f311.jpg",
         "description": "This person is SUPER cool!"
   },
   "29": {
         "name": "Sydney",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362792/00f9f17106a2edacef3f8fbdb8cefe65/166x166-Q90_00f9f17106a2edacef3f8fbdb8cefe65.jpg",
         "description": "This person is SUPER cool!"
   },
   "30": {
         "name": "Talyah",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362798/f4efb833a918980d7a192282fbc95300/166x166-Q90_f4efb833a918980d7a192282fbc95300.jpg",
         "description": "This person is SUPER cool!"
   },
   "31": {
         "name": "Taylor",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362807/ae7a03e228b9da651096cbb75dfd2050/166x166-Q90_ae7a03e228b9da651096cbb75dfd2050.jpg",
         "description": "This person is SUPER cool!"
   },
   "32": {
         "name": "Zoe",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362814/718fd13fc88b8df22d5b74885166ca6c/166x166-Q90_718fd13fc88b8df22d5b74885166ca6c.jpg",
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
      "speakerImage": main_images["host"],
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
      "speakerImage": main_images["bachelor"],
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
      "speakerImage": main_images["host"],
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
      "speakerImage": main_images["host"],
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
      "handbook_q": "TBD",
      "handbook": "TBD",
      "instructions": "Blah Blah", 
      "videos": main_vids["hometowns"]
   },
   "2": {
      "title": "Limo Entrances",
      "roses": 5,
      "contestants": list(range(1, 33)),
      "description": "This is a description of TEST. Hover over people for a description. Then give out your roses one by one. ",
      "nextPage": "/learn/4", 
      "handbook_q": "What are Limousine Entrances?",
      "handbook": "Limousine Entrances are when the contestants meet Joey for the first time! Each woman gets to exit the limo (or whichever vessel they choose) and meet Joey one-on-one, usually introducing herself with a prop that’s significant to her, or her background. It’s important to make a good and lasting impression!",
      "instructions": "Before the roses, click on a girl to check out her limousine entrance!",
      "videos": main_vids["hometowns"]
   },
   "3": {
      "title": "Hometowns",
      "roses": 3,
      "contestants": [1, 2, 3, 4],
      "description": "This is a description of TEST. Hover over people for a description. Then give out your roses one by one. ",
      "nextPage": "/rose/4",
      "handbook_q": "What are hometown visits?",
      "handbook": "Hometown visits are when the bachelor visits the hometown of each of the remaining 4 contestants and meets their families. This is a chance to see how well he blinds with the contestants’ families and for his bond with each contestant to get deeper and stronger. After all the hometown visits, Joey will eliminate 1 of the women in the rose ceremony, so stakes are high!",
      "instructions": "Click each girl to visit their hometown before choosing!",
      "videos": main_vids["hometowns"]
   },
   "4": {
      "title": "Fantasy Suites",
      "roses": 2,
      "contestants": [1, 2, 3],
      "description": "This is a description of TEST. Hover over people for a description. Then give out your roses one by one. ",
      "nextPage": "/rose/5",
      "handbook_q": "What are Fantasy Suites?",
      "handbook": "The Fantasy Suites phase occurs toward the end of each season and takes place in a luxurious setting like a hotel suite or private accommodation. During this stage, the bachelor and the three remaining contestants are given the opportunity to spend private, overnight 1-on-1 dates together without cameras present - a great opportunity for them to deepen their conversations and connections, and discuss more personal matters before the next rose ceremony!",
      "instructions": "Click each girl to get a sneak peek of the dates before choosing!",
      "videos": main_vids["fantasy_suites"]
   },
   "5": {
      "title": "Engagement",
      "roses": 1,
      "contestants": [1, 2],
      "description": "This is a description of TEST. Hover over people for a description. Then give out your roses one by one. ",
      "nextPage": "/quiz",
      "handbook_q": "What happens in the engagement ceremony?",
      "handbook": "During the engagement ceremony, Joey chooses which contestant he will marry, and which he will reject. Each one of the girls will arrive to the engagement spot in an order they don’t know. The first woman is usually the woman that gets broken up with, and the last woman is the one that Joey proposes to. Note: The bachelor doesn’t necessarily need to propose to someone or leave the show with them!",
      "instructions": "Who will be the lucky girl? Who will go home empty-handed?",
      "videos": main_vids["engagement"]
   }
}

quiz_pages = {
   "1": {
      "questionId": "1",
      "question": "In a 2-on-1, what usually happens with the girl that doesn’t get the rose?",
      "questionType": "mult_choice",
      "choices": ["She goes back to the mansion and waits for the next events",
                  "She joins the group date that Joey goes on next",
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
      "question": "A contestant can leave anytime she wants to.",
      "questionType": "true_false",
      "choices": [],
      "answer": ["true"]
   },
   "4": {
      "questionId": "4",
      "question": "The last ceremony doesn’t involve a rose at all.",
      "questionType": "true_false",
      "choices": [],
      "answer": ["true"]
   },
   "5": {
      "questionId": "5",
      "question": "In the engagement ceremony, the bachelor may:",
      "questionType": "mult_select",
      "choices": ["Leave the show unmarried",
                  "Only leave the show married",
                  "Not choose any of the girls",
                  "Choose both of the finalists"],
      "answer": [0, 2, 3]
   },
   "6": {
      "questionId": "6",
      "question": "Drag and drop the major events in order!",
      "questionType": "sort",
      "choices": ["Bachelorette is announced",
                  "Hometowns",
                  "Fantasy Suites",
                  "Visiting Joey's family",
                  "Joey gets engaged"],
      "answer": [1, 2, 4, 3, 0]
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
   global main_images
   data = rose_pages[str(page_num)]
   contestants = []
   for person in data["contestants"]:
      contestants.append(people_list[str(person)])
   return render_template('rose.html', data=data, contestants=contestants, main_images=main_images)

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
def quiz_handler():
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




