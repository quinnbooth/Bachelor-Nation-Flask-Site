from flask import Flask, Response, request, jsonify, render_template
from datetime import datetime
import json
import uuid
import re

app = Flask(__name__)

main_images = {
   "host": "https://scontent-lga3-1.xx.fbcdn.net/v/t1.6435-9/163580111_288668689295431_2707202046743395725_n.jpg?_nc_cat=110&ccb=1-7&_nc_sid=5f2048&_nc_ohc=62bwzzbew-UAb6pIuaB&_nc_ht=scontent-lga3-1.xx&oh=00_AfCPkt3xUkIo7M5b7m4rBqlHmvYQHG2YFmYEFub----_9w&oe=66456A48",
   "bachelor": "https://cdn.vox-cdn.com/thumbor/1NO2SkFoypW9pVXBSzGrADH8Iq8=/1400x1400/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/25213676/BachelorJoey_ABC.jpg",
   "town": "https://www.travelandleisure.com/thmb/Uyakmz5op2sZaMPourbuKi4lYmE=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/telluride-colorado-BESTSMALL0121-22f286c59f7d4077ad15f9359497219f.jpg",
}

# rn, all the same vids for testing
main_vids = {
   "one_date": {
      "Daisy": "https://www.youtube.com/embed/YYvIk0kZeZI?start=180&end=466"
   },
   "two_date": {
      "Maria": "https://www.youtube.com/embed/_Pc_UTIdAPs?start=99&end=404",
      "Sydney": "https://www.youtube.com/embed/YYvIk0kZeZI?start=180&end=466"
   },
   "group_date": {
      "Kelsey A.": "https://www.youtube.com/embed/cpak2-HWohw?si=CdAe7kLk7kSOPHiI&amp;start=106",
      "Rachel": "https://www.youtube.com/embed/xCDc75KHlqY?start=187&end=255",
      "Maria": "https://www.youtube.com/embed/_Pc_UTIdAPs?start=99&end=404",
      "Daisy": "https://www.youtube.com/embed/YYvIk0kZeZI?start=180&end=466",
      "Jess": "https://www.youtube.com/embed/YYvIk0kZeZI?start=180&end=466",
      "Jenn": "https://www.youtube.com/embed/YYvIk0kZeZI?start=180&end=466",
      "Allison": "https://www.youtube.com/embed/YYvIk0kZeZI?start=180&end=466",
      "Autumn": "https://www.youtube.com/embed/YYvIk0kZeZI?start=180&end=466",
      "Chandler": "https://www.youtube.com/embed/YYvIk0kZeZI?start=180&end=466",
   },
   "hometowns": {
      "Kelsey A.": "https://www.youtube.com/embed/cpak2-HWohw?si=CdAe7kLk7kSOPHiI&amp;start=106",
      "Rachel": "https://www.youtube.com/embed/xCDc75KHlqY?si=Z3_dd2HJPcoajTIY&amp;start=147",
      "Maria": "https://www.youtube.com/embed/_Pc_UTIdAPs?si=Q8iKYAL2B0wF-7nd&amp;start=32",
      "Daisy": "https://www.youtube.com/embed/YYvIk0kZeZI?si=kciZF310Hv6-s_Ha&amp;start=43"
   },
   "fantasy_suites": {
      "Kelsey A.": "https://www.youtube.com/embed/5TWOoTRo9YU?si=LMomDWkB_EunBT4X&amp;start=45",
      "Rachel": "https://www.youtube.com/embed/MFJKtDY9vaw?si=c81KEltuAAARxZGb&amp;start=6",
      "Daisy": "https://www.youtube.com/embed/btVOa3tEWs8?si=z_1q3VoqbVgQ6ecJ&amp;start=26"
   },
   "engagement": {
      "Kelsey A.": "https://www.youtube.com/embed/xWIjgu-EQPw?si=5xsDuNFp3SfLr8LJ&amp;start=1",
      "Daisy": "https://www.youtube.com/embed/0UFgP97ScGM?si=OJoXsSg_RwDU9z9I&amp;start=1"
   }
}

people_list = {
   "0": {
         "name": "None",
         "image": "https://t3.ftcdn.net/jpg/05/62/05/20/360_F_562052065_yk3KPuruq10oyfeu5jniLTS4I2ky3bYX.jpg",
         "description": "Discard"
   },
   "1": {
         "name": "Kelsey A.",
         "image": "https://heavy.com/wp-content/uploads/2024/02/kelsey-anderson-bachelor.jpg?quality=65&strip=all",
         "description": "Kelsey A. grew up in Germany on a U.S. military base before moving to the states. Now that she is living in New Orleans, she likes to travel via streetcar and visit the French market."
   },
   "2": {
         "name": "Daisy",
         "image": "https://hips.hearstapps.com/hmg-prod/images/daisy-bio-170217-4395-65ae8e5560c64.jpg?crop=1xw:0.53525xh;center,top&resize=1200:*",
         "description": "Daisy, like Taylor Swift, grew up on a Christmas tree farm. Her parents have been married for over 30 years and she wants to find a lasting love story just like them."
   },
   "3": {
         "name": "Rachel",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362682/e8cffaf4f8b6993e976bac6267b01e48/320x180-Q90_e8cffaf4f8b6993e976bac6267b01e48.jpg",
         "description": "Rachel doesn’t just live in Hawaii like Joey, but she also has Hawaiian roots and is looking forward to discussing Hawaiian food and culture with the bachelor. She also likes “Friends,” Jane Austen books, and hanging out with her friends and family."
   },
   "4": {
         "name": "Maria",
         "image": "https://wegotthiscovered.com/wp-content/uploads/2024/01/The-Bachelorette_-Maria.png",
         "description": "Maria’s official ABC bio describes her as “bold,” and that might be an understatement as the trailer shows her arguing with another woman about spending time with Joey. The Canadian has a black belt in Taekwondo karate, loves spaghetti and enjoys watching horror movies."
   },
   "5": {
         "name": "Allison",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362397/0fa781b5411ff6127e806dedf6e1404b/1000x400-Q90_0fa781b5411ff6127e806dedf6e1404b.jpg",
         "description": "Allison says she is looking for a love story straight out of a rom-com … and she’s willing to compete against her older sister and best friend, Lauren, to find it. The sisters have dated the same guy before, so hopefully their separate connections with Joey won’t put a strain on their relationship."
   },
   "6": {
         "name": "Autumn",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362398/9e3f9d1ccc324feef9ecdac4f6442995/1000x400-Q90_9e3f9d1ccc324feef9ecdac4f6442995.jpg",
         "description": "Autumn, who is twin, comes from a big family in a small town. She loves Coldplay and once got a lip tattoo at a music festival."
   },
   "7": {
         "name": "Chandler",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362399/63f493f17ef609dcd15a4a2f6d698551/166x166-Q90_63f493f17ef609dcd15a4a2f6d698551.jpg",
         "description": "Chandler says she is over dating apps and is ready to find a connection in real life. Her perfect date would be a night baking desserts with her boyfriend."
   },
   "8": {
         "name": "Chrissa",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362404/c6085134bf425c566d33eba2e1e6b36e/166x166-Q90_c6085134bf425c566d33eba2e1e6b36e.jpg",
         "description": "Chrissa is a big fan of Colleen Hoover’s novels, breweries, Scrabble and golf. She was also born on Christmas."
   },
   "9": {
         "name": "Edwina",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362410/cdd1fa5318d92221329b5f4b9a0fa6b7/166x166-Q90_cdd1fa5318d92221329b5f4b9a0fa6b7.jpg",
         "description": "Edwina was born in Liberia and eventually relocated to the United States with her family at the age of 11. She operates a crocheting business and enjoys taking spontaneous trips."
   },
   "10": {
         "name": "Erika",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362411/b6eba7c304b944a540ea5e1279b6a077/166x166-Q90_b6eba7c304b944a540ea5e1279b6a077.jpg",
         "description": "Erika has a dog named Cleo and likes to paint. She is looking for a partner who is adventurous and will visit new restaurants with her."
   },
   "11": {
         "name": "Evalin",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362486/15a41c1653147a5a9dbb1aa8b30b5a16/166x166-Q90_15a41c1653147a5a9dbb1aa8b30b5a16.jpg",
         "description": "Evalin was born in San Antonio, Texas, and has eight siblings. She is a big fan of the musical “Hamilton."
   },
   "12": {
         "name": "Jenn",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362491/6f3352fede1dbd6b6f1634c554871f3b/166x166-Q90_6f3352fede1dbd6b6f1634c554871f3b.jpg",
         "description": "Jenn loves paddleboarding, Taylor Jenkins Reid’s book “The Seven Husbands of Evelyn Hugo” and Shawn Mendes’ music. She is bilingual."
   },
   "13": {
         "name": "Jess",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362515/bdda79724754e41d1edb66e86b292196/166x166-Q90_bdda79724754e41d1edb66e86b292196.jpg",
         "description": "Jess is a big Swiftie and has a Yorkipoo named Charli. “I want to find someone that I can trust my heart with, someone who will respect me, and someone who will do anything to cherish our relationship,” she said."
   },
   "14": {
         "name": "Katelyn",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362576/14a66c5c15561525eb359088e53eac8c/166x166-Q90_14a66c5c15561525eb359088e53eac8c.jpg",
         "description": "Katelyn purchased her first home at just 23 years old. She enjoys a Sarah J. Maas fantasy novel, visiting local cocktail bars and hiking."
   },
   "15": {
         "name": "Kayla",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362582/cc97aaeddc7e86cf64bc82b524b51478/166x166-Q90_cc97aaeddc7e86cf64bc82b524b51478.jpg",
         "description": "Kayla was previously in a serious relationship for eight years. Now, she is hoping to find the man she can spend the rest of her life with. She likes to read “Harry Potter” books, watch “Schitt’s Creek” and spend time with her rescue animals."
   },
   "16": {
         "name": "Kelsey T.",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362600/724db8e0fda6a13e5699f7cc968bb780/166x166-Q90_724db8e0fda6a13e5699f7cc968bb780.jpg",
         "description": "Kelsey T. was previously engaged and she wants to give love another chance. She enjoys playing beach volleyball and listening to Destiny’s Child."
   },
   "17": {
         "name": "Kyra",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362608/bbd18769e19f61942a398734da3a5d98/166x166-Q90_bbd18769e19f61942a398734da3a5d98.jpg",
         "description": "Kyra likes going out to a bar or staying in for a quiet night at home playing Sims equally. She also likes going to the beach and comedy shows."
   },
   "18": {
         "name": "Lanie",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362614/3c08f4afcb9e2816e8d80bcd8f33241d/166x166-Q90_3c08f4afcb9e2816e8d80bcd8f33241d.jpg",
         "description": "Lanie has a large Polish and Greek family and she would love to own a house in Greece. She wants a partner who likes to travel."
   },
   "19": {
         "name": "Lauren",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362618/ea9437fad00456c0f8bcf6802d12f9da/166x166-Q90_ea9437fad00456c0f8bcf6802d12f9da.jpg",
         "description": "Lauren, like her sister Allison, is hoping that Joey is her soulmate. She enjoys working out and going to music festivals."
   },
   "20": {
         "name": "Lea",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362622/2facb01d9e9bbc8f475308c5c3933e58/166x166-Q90_2facb01d9e9bbc8f475308c5c3933e58.jpg",
         "description": "In case viewers forgot, Lea was the contestant that Joey met during “After the Final Rose” when he was announced as the next bachelor. She received a special envelope from Palmer that she will open on night one."
   },
   "21": {
         "name": "Lexi",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362628/b8df1b8af1b7dc1615b1ff10bcdf7b29/166x166-Q90_b8df1b8af1b7dc1615b1ff10bcdf7b29.jpg",
         "description": "Lexi was accepted into an MBA summer program at MIT. As a child, she moved over 15 times. "
   },
   "22": {
         "name": "Madina",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362636/5e195207dc93bf388757cce280fd0e38/166x166-Q90_5e195207dc93bf388757cce280fd0e38.jpg",
         "description": "Madina, who comes from a Bangladeshi family, likes to exercise, dance and watch “The Great British Bake Off.” To relax, she likes to brew a cup of tea and put on a face mask."
   },
   "23": {
         "name": "Marlena",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362659/e757fdeef9bebce993839a0a7c5660c8/166x166-Q90_e757fdeef9bebce993839a0a7c5660c8.jpg",
         "description": "Marlena has a five-year plan that includes being married with two kids and a few rescue dogs. She is looking forward to becoming a soccer mom one day."
   },
   "24": {
         "name": "Nat",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362674/2a5fe05c901758aee25019a2992e2267/166x166-Q90_2a5fe05c901758aee25019a2992e2267.jpg",
         "description": "Nat has a master’s degree. As a nurse, she prioritizes her health ... which means she sleeps for at least 12 hours every night."
   },
   "25": {
         "name": "Sam",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362694/79584baa688bac89bdda0cc67c09eebe/166x166-Q90_79584baa688bac89bdda0cc67c09eebe.jpg",
         "description": "Sam used to live in New York before relocating to the South. She loves pizza and margaritas."
   },
   "26": {
         "name": "Samantha",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362702/5b690e89d3803d2731d659f7aec0b062/166x166-Q90_5b690e89d3803d2731d659f7aec0b062.jpg",
         "description": "Samantha is a cheerleader for the Miami Dolphins and used to dress up as a princess at Disney World. She has competed in pageants."
   },
   "27": {
         "name": "Sandra",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362776/52852754a54ae540d8cbc2cef9e1760e/166x166-Q90_52852754a54ae540d8cbc2cef9e1760e.jpg",
         "description": "Sandra hopes to start a family and become a mom soon. Right now, she enjoys watching “Suits,” traveling and football."
   },
   "28": {
         "name": "Starr",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362782/449fa9825f124fbc031a39c0d581f311/166x166-Q90_449fa9825f124fbc031a39c0d581f311.jpg",
         "description": "Starr likes visiting new restaurants, picnics on the beach and running. She has Brazilian roots and says she can do an impression of Britney Spears."
   },
   "29": {
         "name": "Sydney",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362792/00f9f17106a2edacef3f8fbdb8cefe65/166x166-Q90_00f9f17106a2edacef3f8fbdb8cefe65.jpg",
         "description": "“I am so ready to find my forever person,” Sydney says, per her ABC bio. She is looking for someone who is adventurous and spontaneous. She used to teach English in Thailand."
   },
   "30": {
         "name": "Talyah",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362798/f4efb833a918980d7a192282fbc95300/166x166-Q90_f4efb833a918980d7a192282fbc95300.jpg",
         "description": "Talyah is a fan of “Gossip Girl” and has a chihuahua named Lil Mama. She also doesn’t mind pickup lines."
   },
   "31": {
         "name": "Taylor",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362807/ae7a03e228b9da651096cbb75dfd2050/166x166-Q90_ae7a03e228b9da651096cbb75dfd2050.jpg",
         "description": "Taylor likes hot yoga, ice skating and eating sushi. Like Jenn, she also enjoys reading Taylor Jenkins Reid books."
   },
   "32": {
         "name": "Zoe",
         "image": "https://cdn1.edgedatg.com/aws/v2/abc/TheBachelor/person/4362814/718fd13fc88b8df22d5b74885166ca6c/166x166-Q90_718fd13fc88b8df22d5b74885166ca6c.jpg",
         "description": "Zoe is a sculptor, welder and photographer. Her dream date would be a night at a museum."
   }
}

learn_pages = {
   "1": {
      "text":  '''   Welcome to <b>The Bachelor!</b>\n
                     I’m your host <b><i>Jesse Palmer</i></b>, and in this show, we will help our Bachelor, Joey, find (and possibly marry) his true love over the course of 11 weeks!\n
                     For this, we have selected 32 lucky girls who Joey will have the opportunity to interact with, and choose among as the weeks go by until we are left with 2 special finalists!\n
                     Let’s go ahead and start!
               ''',
      "backgroundImg": "https://media.glamour.com/photos/57aaac377afdb546548e1e69/16:9/w_1632,h_918,c_limit/IMG_7141-1.JPG",
      "speakerImage": main_images["host"],
      "speakerName": "Jesse Palmer",
      "audio": "implement this last if we have time???",
      "nextPage": "/learn/2",
      "timeline": 1
   },
   "2": {
      "text":  '''   Hey there! I'm <b>Joey</b>, a 28-year-old tennis coach living the dream in Hawaii.\n
                     A couple of things about me:\n
                     * Big fan of keeping things chill—drama isn't my game.\n
                     * I'm all about kindness and positive vibes.\n
                     * My biggest fear? Choosing someone who wouldn't choose me back.
               ''',
      "backgroundImg": "https://media.glamour.com/photos/57aaac377afdb546548e1e69/16:9/w_1632,h_918,c_limit/IMG_7141-1.JPG",
      "speakerImage": main_images["bachelor"],
      "speakerName": "Joey",
      "audio": "implement this last if we have time???",
      "nextPage": "/learn/3",
      "timeline": 1  
   },
   "3": {
      "text":  '''   Welcome to the First Week, specifically the First Night!\n
                     Tonight, each woman will make their “limousine entrance” and meet Joey for the first time. \n
                     Continue to learn more about limousine entrances and what else that happens the first night!
               ''',
      "backgroundImg": "https://decider.com/wp-content/uploads/2022/07/LIMO-FEATURE-IMAGE-ENTRANCE.jpg?quality=80&strip=all",
      "speakerImage": main_images["host"],
      "speakerName": "Jesse Palmer",
      "audio": "implement this last if we have time???",
      "nextPage": "/dialogue/1",
      "timeline": 2
   },
   "4": {
      "text":  '''   The first week is over!
                     The next ~7 weeks/episodes will be group dates and 1-on-1’s galore! 
                     We’ll end each episode with a rose ceremony, and we’ll start traveling the world for these dates! \n
                     Oh! Looks like an envelope has arrived for the first of many group dates. 
               ''',
      "backgroundImg": "https://www.travelandleisure.com/thmb/Uyakmz5op2sZaMPourbuKi4lYmE=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/telluride-colorado-BESTSMALL0121-22f286c59f7d4077ad15f9359497219f.jpg",
      "speakerImage": main_images["host"],
      "speakerName": "Jesse Palmer",
      "audio": "implement this last if we have time???",
      "nextPage": "/envelope/1",
      "timeline": 3
   },
   "5": {
      "text":  '''   It's been ~7 weeks and Joey's gotten to know the women so much more through group dates, 1-on-1's and even a 2-on-1! \n
                     After many cocktail parties and rose ceremonies, Joey has now eliminated all but 4 women.\n
                     Now, we'll begin Hometowns, a huge milestone in Joey's relationship with each woman.  
               ''',
      "backgroundImg": "https://www.travelandleisure.com/thmb/Uyakmz5op2sZaMPourbuKi4lYmE=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/telluride-colorado-BESTSMALL0121-22f286c59f7d4077ad15f9359497219f.jpg",
      "speakerImage": main_images["host"],
      "speakerName": "Jesse Palmer",
      "audio": "implement this last if we have time???",
      "nextPage": "/dialogue/2",
      "timeline": 3
   },
   "6": {
      "text":  '''   Things are really amping up! Now it's time for fantasy suites. \n\nContinue to learn about this milestone!  
               ''',
      "backgroundImg": "https://www.travelandleisure.com/thmb/Uyakmz5op2sZaMPourbuKi4lYmE=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/telluride-colorado-BESTSMALL0121-22f286c59f7d4077ad15f9359497219f.jpg",
      "speakerImage": main_images["host"],
      "speakerName": "Jesse Palmer",
      "audio": "implement this last if we have time???",
      "nextPage": "/dialogue/3",
      "timeline": 3
   },
   "7": {
      "text":  '''   And finally, with 2 women left, it's time for the engagement, the final rose ceremony. 
               ''',
      "backgroundImg": "https://www.travelandleisure.com/thmb/Uyakmz5op2sZaMPourbuKi4lYmE=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/telluride-colorado-BESTSMALL0121-22f286c59f7d4077ad15f9359497219f.jpg",
      "speakerImage": main_images["host"],
      "speakerName": "Jesse Palmer",
      "audio": "implement this last if we have time???",
      "nextPage": "/dialogue/4",
      "timeline": 3
   },
   "8": {
      "text":  '''   Great job!\n
                     You've helped Joey make it through all the events.\n
                     The engagement happens in the final episode of the season. This episode also features a studio portion filmed about 6 months after. Everyone you know and loves comes back to join me in watching the engagement. We'll also hear from our final couple post-engagement!\n\nI also announce the new Bachelorette, who is always from the current season's pool of contestants, and usually a runner-up or fan-favorite. She'll be in Joey's position and finding love from her own batch of new contestants. 
               ''',
      "backgroundImg": "https://media.glamour.com/photos/57aaac377afdb546548e1e69/16:9/w_1632,h_918,c_limit/IMG_7141-1.JPG",
      "speakerImage": main_images["host"],
      "speakerName": "Jesse Palmer",
      "audio": "implement this last if we have time???",
      "nextPage": "/learn/9",
      "timeline": 9
   },
   "9": {
      "text":  '''   Now let's see if you've really become an expert on The Bachelor...
               ''',
      "backgroundImg": "https://media.glamour.com/photos/57aaac377afdb546548e1e69/16:9/w_1632,h_918,c_limit/IMG_7141-1.JPG",
      "speakerImage": main_images["host"],
      "speakerName": "Jesse Palmer",
      "audio": "implement this last if we have time???",
      "nextPage": "/quiz",
      "timeline": 9
   }
}

rose_pages = {
   "2": {
      "title": "Limo Entrances",
      "roses": 5,
      "contestants": list(range(1, 33)),
      "description": "This is a description of TEST. Hover over people for a description. Then give out your roses one by one. ",
      "nextPage": "/learn/4", 
      "handbook_q": "What are Limousine Entrances?",
      "handbook": "Limousine Entrances are when the contestants meet Joey for the first time! Each woman gets to exit the limo (or whichever vessel they choose) and meet Joey one-on-one, usually introducing herself with a prop that’s significant to her, or her background. It’s important to make a good and lasting impression!",
      "instructions": "Before the roses, click on a girl to check out her limousine entrance!",
      "videos": main_vids["hometowns"],
      "timeline": 2
   },
   "3": {
      "title": "Group Dates",
      "roses": 1,
      "contestants": [1, 2, 3, 4, 5, 6, 7],
      "description": "This is a description of TEST. Hover over people for a description. Then give out your roses one by one. ",
      "nextPage": "/envelope/2",
      "handbook_q": "What is a group date?",
      "handbook": "As it, sounds, a group date takes place when the bachelor chooses a set of girls he wants a group date with. He always excludes the contestant that was chosen for the 1-on-1 though, and does not include all the remaining women. Usually, the Bachelor will try to space it out so that if a woman is not chosen in one group date, she will be chosen on the next, but this is all up to the Bachelor’s discretion. In group dates, a group activity usually takes place, followed by a group cocktail party in which they can get some alone convo time with him. The bachelor can decide if he gives one or more roses - if a girl receives a rose, she will automatically have made it to the next round, and if not, she will have to wait for the rose ceremony to see if she will get a rose.",
      "instructions": "Click each girl to get a sneak peek of the dates before choosing!",
      "videos": main_vids["group_date"],
      "timeline": 3
   },
   "4": {
      "title": "1-1 Dates",
      "roses": 1,
      "contestants": [2, 0],
      "description": "This is a description of TEST. Hover over people for a description. Then give out your roses one by one. ",
      "nextPage": "/envelope/3",
      "handbook_q": "What is a 1-1 Date?",
      "handbook": "The bachelor usually selects a lucky contestant to go on the 1-on-1 date, and his date invitation is sent to the mansion, opened by all the women. In a 1-on-1 date, Joey and the lucky contestant will go on a romantic daytime date, planned by him, which always ends in a dinner date where the couple can really talk and open up to each other. Then the bachelor decides if he gives his date a rose or not, and if she does, she automatically makes it to the next round - she will not need to participate in the rose ceremony",
      "instructions": "Click each girl to get a sneak peek of the dates before choosing!",
      "videos": main_vids["one_date"],
      "timeline": 4
   },
   "5": {
      "title": "2-1 Dates",
      "roses": 1,
      "contestants": [4, 29],
      "description": "This is a description of TEST. Hover over people for a description. Then give out your roses one by one. ",
      "nextPage": "/learn/5",
      "handbook_q": "What is a 2-on-1 date?",
      "handbook": "It’s a special kind of date, in which two women are invited by the bachelor to go on a date together. They follow the same flow as the 1-on-1 date, where they have a day-time date, and then a dinner at night, in which a rose is handed out. The 2 -on-1 date is special because only 1 rose is handed out, and the woman who does not receive the rose has to immediately go home. She doesn't even get to go back to the mansion, as prior to the date, both women pack up their belongings so that when the Bachelor makes his decision, the rejected woman’s luggage is removed by staff. The 2-on-1 is used on rare occasion, and this season, it was arranged because there was drama between Maria and Sydney, and Joey needed to get to the bottom of it.",
      "instructions": "Click each girl to get a sneak peek of the dates before choosing!",
      "videos": main_vids["two_date"],
      "timeline": 5
   },
   "6": {
      "title": "Hometowns",
      "roses": 3,
      "contestants": [1, 2, 3, 4],
      "description": "This is a description of TEST. Hover over people for a description. Then give out your roses one by one. ",
      "nextPage": "/rose/7",
      "handbook_q": "What are hometown visits?",
      "handbook": "Hometown visits are when the bachelor visits the hometown of each of the remaining 4 contestants and meets their families. This is a chance to see how well he blinds with the contestants’ families and for his bond with each contestant to get deeper and stronger. After all the hometown visits, Joey will eliminate 1 of the women in the rose ceremony, so stakes are high!",
      "instructions": "Click each girl to visit their hometown before choosing!",
      "videos": main_vids["hometowns"],
      "timeline": 6
   },
   "7": {
      "title": "Fantasy Suites",
      "roses": 2,
      "contestants": [1, 2, 3],
      "description": "This is a description of TEST. Hover over people for a description. Then give out your roses one by one. ",
      "nextPage": "/rose/8",
      "handbook_q": "What are Fantasy Suites?",
      "handbook": "The Fantasy Suites phase occurs toward the end of each season and takes place in a luxurious setting like a hotel suite or private accommodation. During this stage, the bachelor and the three remaining contestants are given the opportunity to spend private, overnight 1-on-1 dates together without cameras present - a great opportunity for them to deepen their conversations and connections, and discuss more personal matters before the next rose ceremony!",
      "instructions": "Click each girl to get a sneak peek of the dates before choosing!",
      "videos": main_vids["fantasy_suites"],
      "timeline": 7
   },
   "8": {
      "title": "Engagement",
      "roses": 1,
      "contestants": [1, 2, 0],
      "description": "This is a description of TEST. Hover over people for a description. Then give out your roses one by one. ",
      "nextPage": "/learn/6",
      "handbook_q": "What happens in the engagement ceremony?",
      "handbook": "During the engagement ceremony, Joey chooses which contestant he will marry, and which he will reject. Each one of the girls will arrive to the engagement spot in an order they don’t know. The first woman is usually the woman that gets broken up with, and the last woman is the one that Joey proposes to. Note: The bachelor doesn’t necessarily need to propose to someone or leave the show with them!",
      "instructions": "Who will be the lucky girl? Who will go home empty-handed?",
      "videos": main_vids["engagement"],
      "timeline": 8
   }
}


# Number the pieces of dialogue however you want (no repeat ids). The order you type them here determines their placement. Odd number = Left. Even number = Right.
dialogue_pages = {
   "1": {
      "1": {
         "speakerName": "Jesse Palmer",
         "speakerImage": main_images['host'],
         "dialogue": "Hey Joey, happy first night! We're here at the Bachelor Mansion. Ready to learn about Limousine Entrances?"
      },
      "2": {
         "speakerName": "Joey",
         "speakerImage": main_images['bachelor'],
         "dialogue": "Thanks Jesse! Yes, what happens during these entrances?"
      },
      "3": {
         "speakerName": "Jesse Palmer",
         "speakerImage": main_images['host'],
         "dialogue": "Each contestant has the chance to exit a limo (or their vehicle of choice), usually with a special prop to make a memorable first impression!"
      },
      "5": {
         "speakerName": "Jesse Palmer",
         "speakerImage": main_images['host'],
         "dialogue": "One contestant pulled up in a boat this season, and another pulled up in a truck lugging a Christmas tree, since she grew up on a tree farm. Other contestants stuck with the limo but brought things like a voodoo doll for their hometown NOLA, or a chemistry set to represent their studies. There's always a catchy pick-up line!\nHere's an example!",
      },
      "7": {
         "speakerName": "Jesse Palmer",
         "speakerImage": main_images['host'],
         "dialogue": "",
         "videoURL": "https://www.youtube.com/embed/pSiGVuIAwI0?si=_lEgpnNiv86H4u2i&start=1"
      },
      "8": {
         "speakerName": "Joey",
         "speakerImage": main_images['bachelor'],
         "dialogue": "Sounds like a key moment for them and me. What happens the rest of the night?"
      },
      "9": {
         "speakerName": "Jesse Palmer",
         "speakerImage": main_images['host'],
         "dialogue": "After the limo entrances, you'll have your first group cocktail party. The women will have already gathered inside the mansion following their entrances, and now will have the chance to grab you and talk to you one-on-one."
      },
      "10": {
         "speakerName": "Jesse Palmer",
         "speakerImage": main_images['host'],
         "dialogue": "Finally, you'll have your first rose ceremony too, where you'll choose the women you want to stay based off this first night by handing them a rose. Contestants without a rose will be sent home. And, remember it's not just you picking throughout the experience. Each contestant can go home at any time she chooses to."
      },
      "backgroundImg": main_images["town"],
      "nextPage": "/learn/4",
      "timeline": 1,
      # rose data 
      "rose_data": rose_pages["2"]
   },
   "2": {
      "2": {
         "speakerName": "Joey",
         "speakerImage": main_images['bachelor'],
         "dialogue": "Jesse, what happens during the hometown visits?"
      },
      "3": {
         "speakerName": "Jesse Palmer",
         "speakerImage": main_images['host'],
         "dialogue": "Hometowns are key, Joey. You’ll visit the hometown of each of the final four contestants to meet their families."
      },
      "4": {
         "speakerName": "Joey",
         "speakerImage": main_images['bachelor'],
         "dialogue": "Sounds important. What’s the goal of these visits?"
      },
      "5": {
         "speakerName": "Jesse Palmer",
         "speakerImage": main_images['host'],
         "dialogue": "It’s a chance to see how well you blend with their families and to deepen your bond with each contestant. Remember, after these visits, you’ll have to make a tough decision at the rose ceremony where one woman will go home."
      },
      "6": {
         "speakerName": "Joey",
         "speakerImage": main_images['bachelor'],
         "dialogue": "It's getting serious. Thanks for the insight, Jesse. I’ll do my best to follow my gut instincts."
      }, 
      "backgroundImg": main_images["town"],
      "nextPage": "/learn/6",
      "timeline": 6,
      # rose data 
      "rose_data": rose_pages["6"]
   },
   "3": {
      "1": {
         "speakerName": "Jesse Palmer",
         "speakerImage": main_images['host'],
         "dialogue": "Joey, it's time for Fantasy Suites. It’s a really special part of the show. Do you know what happens?"
      },
      "2": {
         "speakerName": "Joey",
         "speakerImage": main_images['bachelor'],
         "dialogue": "I know a little, Jesse, but can you tell me more?"
      },
      "3": {
         "speakerName": "Jesse Palmer",
         "speakerImage": main_images['host'],
         "dialogue": "Sure thing. You and the last three contestants will have private overnight dates in really nice places, like a hotel suite. There won’t be any cameras, so it’s just you guys."
      },
      "4": {
         "speakerName": "Joey",
         "speakerImage": main_images['bachelor'],
         "dialogue": "That sounds like a good chance to really see how we get along. What should I think about during these dates?"
      },
      "5": {
         "speakerName": "Jesse Palmer",
         "speakerImage": main_images['host'],
         "dialogue": "Use this time to talk about personal stuff and what you both want in the future. It’s important to know what you need in a partner before the next rose ceremony. After this, you'll be down to 2 women."
      },
      "backgroundImg": main_images["town"],
      "nextPage": "/learn/7",
      "timeline": 7,
      # rose data 
      "rose_data": rose_pages["7"]
   },
   "4": {
      "1": {
         "speakerName": "Jesse Palmer",
         "speakerImage": main_images['host'],
         "dialogue": "Joey, next up is the engagement ceremony. It's a big moment. Are you clear on how it works?"
      },
      "2": {
         "speakerName": "Joey",
         "speakerImage": main_images['bachelor'],
         "dialogue": "I think so, but can you go over the details one more time?"
      },
      "3": {
         "speakerName": "Jesse Palmer",
         "speakerImage": main_images['host'],
         "dialogue": "Absolutely. Before the actual ceremony, each of the remaining 2 women will get to meet your family and have a last 1-on-1 date with you. Then, during the ceremony, each of the final contestants arrives at the engagement spot in an unknown order. Traditionally, the first woman to arrive is usually not the one chosen, and the last one is who you might propose to."
      },
      "4": {
         "speakerName": "Joey",
         "speakerImage": main_images['bachelor'],
         "dialogue": "Got it. And I don’t have to propose if it doesn’t feel right, correct?"
      },
      "5": {
         "speakerName": "Jesse Palmer",
         "speakerImage": main_images['host'],
         "dialogue": "Exactly right, Joey. And if you do propose, you'll do it with a ring from our ring designer Neil Lane and with a final rose. Just remember, this is a huge step, and whatever you decide, make sure it feels right. You’ve got this! Everyone’s rooting for you to find your true happiness."
      },
      "backgroundImg": main_images["town"],
      "nextPage": "/learn/8",
      "timeline": 8,
      # rose data 
      "rose_data": rose_pages["8"]

   }
}

envelope_pages = {
   "1": {
   "text":  '''   To Maria, Jenn, Autumn, …, Kelsey A., 
                  Get in your tennis gear and join me for a group date!
                  Love, Joey
            ''',
   "audio": "implement this last if we have time???",
   "nextPage": "/rose/3",
   "timeline": 3
   },
   "2": {
      "text":  '''   Dear Daisy,
                     I really enjoyed our time last night. Join me for a 1-on-1? 
                     Love, Joey
               ''',
      "audio": "implement this last if we have time???",
      "nextPage": "/rose/4",
      "timeline": 4
   },
   "3": {
      "text":  '''   To Maria and Sydney, 
                     I would love to clear the air, join me for a 2-on-1?
                     Love, Joey
               ''',
      "audio": "implement this last if we have time???",
      "nextPage": "/rose/5",
      "timeline": 5
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
      "answer": [3],
      "timeline": 9
   },
   "2": {
      "questionId": "2",
      "question": "What is the name of our host?",
      "questionType": "fill_blank",
      "choices": [],
      "answer": ["Jesse Palmer"],
      "timeline": 9
   },
   "3": {
      "questionId": "3",
      "question": "A contestant can leave anytime she wants to.",
      "questionType": "true_false",
      "choices": [],
      "answer": ["true"],
      "timeline": 9
   },
   "4": {
      "questionId": "4",
      "question": "The last ceremony doesn’t involve a rose at all.",
      "questionType": "true_false",
      "choices": [],
      "answer": ["false"],
      "timeline": 9
   },
   "5": {
      "questionId": "5",
      "question": "In the engagement ceremony, what can the bachelor do? Select all that apply:",
      "questionType": "mult_select",
      "choices": ["Leave the show unmarried",
                  "Only leave the show married",
                  "Not choose any of the girls",
                  "Choose both of the finalists"],
      "answer": [0, 2, 3],
      "timeline": 9
   },
   "6": {
      "questionId": "6",
      "question": "Drag and drop the major events in order!",
      "questionType": "sort",
      "choices": ["Bachelorette is announced",
                  "Hometowns",
                  "Fantasy Suites",
                  "Meeting Joey's family",
                  "Joey gets engaged"],
      "answer": [1, 2, 3, 4, 0],
      "timeline": 9
   }
}


# Sets used to keep track of which questions user got correct / incorrect in quiz section
correct = list()
incorrect = list()
answers = [None, None, None, None, None, None]

# Times the user visited each page
timestamps = []

#####################      ROUTES      #####################

@app.before_request
def before_request():
   if "static" in request.path:
      return 
   timestamps.append((request.path, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
   print("\nVISIT LOG:", timestamps)

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

@app.route('/dialogue/<page_num>')
def dialogue(page_num):
   global dialogue_pages
   global people_list
   global main_images
   data = dialogue_pages[str(page_num)]
   contestants = []
   for person in data["rose_data"]["contestants"]:
      contestants.append(people_list[str(person)])
   is_first_page = (page_num == '1')
   return render_template('dialogue.html', data=data, contestants=contestants, main_images=main_images, rose_data=data["rose_data"], is_first_page=is_first_page)

@app.route('/envelope/<page_num>')
def envelope(page_num):
   global envelope_pages
   data = envelope_pages[str(page_num)]
   return render_template('envelope.html', data=data)

@app.route('/quiz')
def quiz_home():
   global correct
   global incorrect
   data = {
      "correct": correct,
      "incorrect": incorrect,
      "timeline": 9
   }
   return render_template('quiz_home.html', data=data, answers=answers)

@app.route('/quiz/<page_num>')
def quiz(page_num):
   global quiz_pages
   data = quiz_pages[str(page_num)]
   global correct
   global incorrect
   return render_template('quiz.html', data=data, correct=correct, incorrect=incorrect, answers=answers)   

#####################  AJAX FUNCTIONS  #####################

@app.route('/quiz_handler', methods=['POST'])
def quiz_handler():
   global correct
   global incorrect
   global answers
   json_data = request.get_json()
   isCorrect = json_data["isCorrect"]
   question_id = json_data["id"]
   answers[int(question_id) - 1] = json_data["answer"]
   
   if isCorrect:
      correct.append(question_id)
   else:
      incorrect.append(question_id)
            
   return jsonify({'redirect': '/quiz'})

############################################################

if __name__ == '__main__':
   app.run(debug = True, port=5001)




