import cv2
import os
import numpy as np
import requests
import faceRecognition as fr
from flask import Flask, request, render_template, url_for, redirect
from flask_mysqldb import MySQL
from bs4 import BeautifulSoup
from os.path import abspath

app = Flask(__name__)

		# ----------------- Set up of Database ----------------- #

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'FightersDB'	
mysql = MySQL(app)

@app.route("/")
def fileFrontPage():
	cur = mysql.connection.cursor()
	cur.execute("CREATE DATABASE IF NOT EXISTS FightersDB")
	#cur.execute("use FightersDB")
	cur.execute("CREATE TABLE IF NOT EXISTS Fighters (fighter_id int AUTO_INCREMENT NOT NULL, fullname VARCHAR(30) NULL, DOB VARCHAR(30) NULL, Nationality VARCHAR(30) NULL, Record VARCHAR(30) NULL, Accomplishment VARCHAR(30) NULL, PRIMARY KEY(fighter_id)) ")
	cur.execute("CREATE TABLE IF NOT EXISTS Fights (fight_id int AUTO_INCREMENT NOT NULL, fullname VARCHAR(30) NULL, opponent VARCHAR(30) NULL, fighter1_id int NOT NULL, fighter2_id int NOT NULL, outcome VARCHAR(30) NULL, PRIMARY KEY(fight_id), FOREIGN KEY(fighter1_id) REFERENCES Fighters(fighter_id),FOREIGN KEY(fighter2_id) REFERENCES Fighters(fighter_id))")
	cur.execute("SELECT * FROM Fighters ")
	data = cur.fetchall()
	mysql.connection.commit()
	return render_template("fileform.html", valueList=data)

@app.route("/handleUpload", methods=['POST'])
def handleFileUpload():
	
		#--------------------- AI Training Images and Identification ----------------------#
	
	if 'photo' in request.files:
		photo = request.files['photo']
		if photo.filename != '':            
			# Change from Relative Path to Absolute Path
			filePath = abspath('../Face Recognition OpenCV with Fighters DataBase/uploads')
			picSelected = os.path.join(filePath, photo.filename)
			print(picSelected)
			test_img = cv2.imread(picSelected)
			
			# Set variables to faceDetection function from fr.py
			faces_detected,gray_img=fr.faceDetection(test_img)
			print("faces_detected", faces_detected)
			
			# Drawing the rectangle around faces when detecting it
			#..for (x,y,w,h) in faces_detected:
				# parameter as test_img because we want to display the bounding boxes, using function rectangle
				# x and y are the diagonal points to form around the faces that will be detected, h and w: height and width
				#..cv2.rectangle(test_img, (x,y), (x+w, y+h), (255,0,0), thickness=5)
				
			# Resizing image and showing it
			#..resized_img = cv2.resize(test_img,(500,350))
			#..cv2.imshow("face detectuib tutorial", resized_img)

			# Wait until any key is pressed and exit
			#..cv2.waitKey(0)
			#..cv2.destroyAllWindows
			
			trainPath = abspath('../Face Recognition OpenCV with Fighters DataBase/Training Images')
			faces,faceID = fr.labels_for_training_data(trainPath)
			face_recognizer = fr.train_classifier(faces,faceID)
			face_recognizer.save('trainingData.yml')
			name = {0:"Manny Pacquiao",1:"Floyd Mayweather Jr",2:"Conor McGregor",3:"Saul Alvarez",4:"Unknown"}
			predicted_name = 'Unknown'
			
			for face in faces_detected:
				(x,y,w,h) = face					# The coordinates for a single face
				roi_gray = gray_img[y:y+h,x:x+h]	# Extract the gray image that we detected, which is face
	
				# returns a label (0 or 1) and confidence value from predict func (openCV)
				# If confidence value = 0 then exact match, if more than 35 then don't want to predict that value because it is wrong
				label,confidence = face_recognizer.predict(roi_gray)
				print("confidence: ", confidence)
				print("label: ", label)
	
				# call draw_rect which will draw a rectangle box on our image
				fr.draw_rect(test_img,face)
	
				# based on list name and label, name is predicted
				predicted_name = name[label]
	
				# Putting the text into the image along with its coordinates
				fr.put_text(test_img,predicted_name,x,y)
				
			resized_img = cv2.resize(test_img,(500,350))
			cv2.imshow("face detectuib tutorial", resized_img)
			
			if predicted_name == 'Manny Pacquiao':
				print("The person in the picture is Manny")
			elif predicted_name == 'Floyd Mayweather Jr':
				print("The person in the picture is Floyd")
			elif predicted_name == 'Conor McGregor':
				print("The person in the picture is Conor")
			elif predicted_name == 'Saul Alvarez':
				print("The person in the picture is Saul")
			else:
				print("Unknown person")
				
			#--------------------- Web Scrapping Boxrec.com ----------------------#	
				
			Mayweather_url = requests.get('http://boxrec.com/en/boxer/352')
			Pacquiao_url = requests.get('http://boxrec.com/en/boxer/6129')
			McGregor_url = requests.get('http://boxrec.com/en/boxer/802658')
			Canelo_url = requests.get('http://boxrec.com/en/boxer/348759')

			MayweatherSoup = BeautifulSoup(Mayweather_url.content, 'html.parser')
			PacquiaoSoup = BeautifulSoup(Pacquiao_url.content, 'html.parser')
			McGregorSoup = BeautifulSoup(McGregor_url.content, 'html.parser')
			CaneloSoup = BeautifulSoup(Canelo_url.content, 'html.parser')
			#print(soup.prettify())

			Floydtable = MayweatherSoup.find('table',class_='dataTable')
			Mannytable = PacquiaoSoup.find('table',class_='dataTable')
			Conortable = McGregorSoup.find('table',class_='dataTable')
			Saultable = CaneloSoup.find('table',class_='dataTable')
			#print(My_table)

			FloydNames = Floydtable.findAll(class_='personLink')
			FloydBouts = Floydtable.findAll(class_='boutResult')

			MannyNames = Mannytable.findAll(class_='personLink')
			MannyBouts = Mannytable.findAll(class_='boutResult')

			ConorNames = Conortable.findAll(class_='personLink')
			ConorBouts = Conortable.findAll(class_='boutResult')

			SaulNames = Saultable.findAll(class_='personLink')
			SaulBouts = Saultable.findAll(class_='boutResult')
			
			FloydOpponents = []
			FloydOutcomes = []

			MannyOpponents = []
			MannyOutcomes = []

			ConorOpponents = []
			ConorOutcomes = []

			SaulOpponents = []
			SaulOutcomes = []

			for name in FloydNames:
				FloydOpponents.append(name.text)

			for bout in FloydBouts:
				FloydOutcomes.append(bout.text)
				
			for name in MannyNames:
				MannyOpponents.append(name.text)

			for bout in MannyBouts:
				MannyOutcomes.append(bout.text)
				
			for name in ConorNames:
				ConorOpponents.append(name.text)

			for bout in ConorBouts:
				ConorOutcomes.append(bout.text)
				
			for name in SaulNames:
				SaulOpponents.append(name.text)

			for bout in SaulBouts:
				SaulOutcomes.append(bout.text)

			FloydResults = dict(zip(FloydOpponents, FloydOutcomes))
			MannyResults = dict(zip(MannyOpponents, MannyOutcomes))
			ConorResults = dict(zip(ConorOpponents, ConorOutcomes))
			SaulResults = dict(zip(SaulOpponents, SaulOutcomes))
			
			# Wait until any key is pressed and exit
			cv2.waitKey(0)
			cv2.destroyAllWindows
			
		#------------------- Info Scrapped into Database and Webpage HTML ---------------------#
			
			if predicted_name == 'Manny Pacquiao':
				@app.route('/', methods=['GET', 'POST'])
				def index():
					fullname = "Manny Pacquiao"
					cur = mysql.connection.cursor()
					#cur.execute("INSERT INTO Fighters (fullname, DOB, Nationality, Record, Accomplishment) SELECT * FROM (SELECT 'Manny Pacquiao', 'Dec 17, 1978', 'Filipino', '61-2-7', '8-time Boxing Champion') AS tmp WHERE NOT EXISTS (SELECT fullname FROM Fighters WHERE fullname = 'Manny Pacquiao') LIMIT 1")
					cur.execute("UPDATE Fighters SET DOB = 'Dec 17, 1978', Nationality = 'Filipino', Record = '61-2-7', Accomplishment = '8-time Boxing Champion' WHERE fullname = 'Manny Pacquiao'")
					cur.execute("SELECT fighter_id FROM Fighters WHERE fullname = 'Manny Pacquiao'")
					MannyID = cur.fetchone()
					for x,y in MannyResults.items():
						result = cur.execute("INSERT INTO Fighters (fullname) SELECT * FROM (SELECT %s ) AS tmp WHERE NOT EXISTS (SELECT fullname FROM Fighters WHERE fullname = %s) LIMIT 1", (x, x))	
						#cur.execute("SELECT MAX(fighter_id) FROM Fighters")
						cur.execute("SELECT fighter_id FROM Fighters WHERE fullname = %s", (x,))
						myresult = cur.fetchone()
						myresult = int(myresult[0])	# convert tuple into int
						#print(myresult)
						print(x)
						print(y)
						cur.execute("INSERT INTO Fights(fullname, opponent, fighter1_id, fighter2_id, outcome) SELECT * FROM (SELECT 'Manny Pacquiao', %s, %s, %s, %s) AS tmp WHERE NOT EXISTS (SELECT fighter_id FROM Fighters WHERE fullname = 'Manny Pacquiao')", (x, MannyID, myresult, y,))
					cur.execute("SELECT * FROM Fights WHERE fullname = 'Manny Pacquiao'")
					data = cur.fetchall()
					mysql.connection.commit()
					cur.close()
					return render_template("index.html", value=data)
					
			elif predicted_name == 'Floyd Mayweather Jr':
				@app.route('/', methods=['GET', 'POST'])
				def index():
					cur = mysql.connection.cursor()
					cur.execute("INSERT INTO Fighters (fighter_id, fullname, DOB, Nationality, Record, Accomplishment) SELECT * FROM (SELECT '1','Floyd Mayweather Jr', 'Feb 24 1977', 'American', '50-0', 'Retired Undefeated') AS tmp WHERE NOT EXISTS (SELECT fullname FROM Fighters WHERE fullname = 'Floyd Mayweather Jr') LIMIT 1")
					for x,y in FloydResults.items():
						result = cur.execute("INSERT INTO Fighters (fullname) SELECT * FROM (SELECT %s ) AS tmp WHERE NOT EXISTS (SELECT fullname FROM Fighters WHERE fullname = %s) LIMIT 1", (x, x))	
						#cur.execute("SELECT MAX(fighter_id) FROM Fighters")
						cur.execute("SELECT fighter_id FROM Fighters WHERE fullname = %s", (x,))
						myresult = cur.fetchone()
						myresult = int(myresult[0])	# convert tuple into int
						print(myresult)
						print(x)
						#cur.execute("INSERT INTO Fights(fullname, opponent, fighter1_id, fighter2_id) SELECT * FROM (SELECT 'Floyd Mayweather Jr', %s, '1', %s) AS tmp WHERE EXISTS (SELECT fighter_id FROM Fighters WHERE fullname = 'Floyd Mayweather Jr') LIMIT 1", (x, myresult,))
						cur.execute("INSERT INTO Fights(fullname, opponent, fighter1_id, fighter2_id, outcome) SELECT * FROM (SELECT 'Floyd Mayweather Jr', %s, '1', %s, %s) AS tmp WHERE NOT EXISTS (SELECT fighter_id FROM Fighters WHERE fullname = 'Floyd Mayweather Jr') ", (x, myresult, y))
					cur.execute("SELECT * FROM Fights WHERE fullname = 'Floyd Mayweather Jr'")
					data = cur.fetchall()
					mysql.connection.commit()
					cur.close()
					return render_template("index.html", value=data)
			
			elif predicted_name == 'Conor McGregor':
				@app.route('/', methods=['GET', 'POST'])
				def index():
					fullname = "Conor McGregor"
					cur = mysql.connection.cursor()
					#cur.execute( "INSERT INTO Fighters (fighter_id, fullname, DOB, Nationality, Record, Accomplishment) SELECT * FROM (SELECT '3','Conor McGregor', 'July 14 1988', 'Irish', '21-4', '2-time UFC Champion' ) AS tmp WHERE NOT EXISTS (SELECT fullname FROM Fighters WHERE fullname = 'Conor McGregor') LIMIT 1")
					cur.execute("UPDATE Fighters SET DOB = 'July 14 1988', Nationality = 'Irish', Record = '0-1', Accomplishment = '2-time UFC Champion' WHERE fullname = 'Conor McGregor'")
					cur.execute("SELECT fighter_id FROM Fighters WHERE fullname = 'Conor McGregor'")
					ConorID = cur.fetchone()
					for x,y in ConorResults.items():
						result = cur.execute("INSERT INTO Fighters (fullname) SELECT * FROM (SELECT %s ) AS tmp WHERE EXISTS (SELECT fullname FROM Fighters WHERE fullname = %s) LIMIT 1", (x, x))	
						cur.execute("SELECT fighter_id FROM Fighters WHERE fullname = %s", (x,))
						myresult = cur.fetchone()
						myresult = int(myresult[0])	# convert tuple into int
						print(myresult)
						print(x)
						cur.execute("INSERT INTO Fights(fullname, opponent, fighter1_id, fighter2_id, outcome) SELECT * FROM (SELECT 'Conor McGregor', %s, %s, %s, %s) AS tmp WHERE EXISTS (SELECT fighter_id FROM Fighters WHERE fullname = 'Conor McGregor') LIMIT 1", (x, ConorID, myresult, y))
					cur.execute("SELECT * FROM Fights WHERE fullname = 'Conor McGregor'")
					data = cur.fetchall()
					mysql.connection.commit()
					cur.close()
					return render_template("index.html", value=data)
			
			elif predicted_name == 'Saul Alvarez':
				@app.route('/', methods=['GET', 'POST'])
				def index():
					cur = mysql.connection.cursor()
					#cur.execute( "INSERT INTO Fighters (fighter_id, fullname, DOB, Nationality, Record, Accomplishment) SELECT * FROM (SELECT '4','Saul Alvarez', 'July 18 1990', 'Mexican', '52-2-1', '2nd Youngest Champ') AS tmp WHERE NOT EXISTS (SELECT fullname FROM Fighters WHERE fullname = 'Saul Alvarez') LIMIT 1")
					cur.execute("UPDATE Fighters SET DOB = 'July 18 1990', Nationality = 'Mexican', Record = '52-2-1', Accomplishment = '2nd Youngest Champion' WHERE fullname = 'Saul Alvarez'")
					cur.execute("SELECT fighter_id FROM Fighters WHERE fullname = 'Saul Alvarez'")
					SaulID = cur.fetchone()
					for x,y in SaulResults.items():
						result = cur.execute("INSERT INTO Fighters (fullname) SELECT * FROM (SELECT %s ) AS tmp WHERE NOT EXISTS (SELECT fullname FROM Fighters WHERE fullname = %s) LIMIT 1", (x, x))	
						cur.execute("SELECT fighter_id FROM Fighters WHERE fullname = %s", (x,))
						myresult = cur.fetchone()
						myresult = int(myresult[0])	# convert tuple into int
						print(myresult)
						print(x)
						cur.execute("INSERT INTO Fights(fullname, opponent, fighter1_id, fighter2_id, outcome) SELECT * FROM (SELECT 'Saul Alvarez', %s, %s, %s, %s) AS tmp WHERE EXISTS (SELECT fighter_id FROM Fighters WHERE fullname = 'Saul Alvarez') LIMIT 1", (x, SaulID, myresult, y))
					cur.execute("SELECT * FROM Fights WHERE fullname = 'Saul Alvarez'")
					data = cur.fetchall()
					mysql.connection.commit()
					cur.close()
					return render_template("index.html", value=data)
					
			else:
				@app.route('/', methods=['GET', 'POST'])
				def index():
					cur = mysql.connection.cursor()
					cur.execute("SELECT * FROM Fighters ")
					data = cur.fetchall()
					mysql.connection.commit()
					cur.close()
					return render_template("index.html", valueList=data)
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM Fights WHERE fullname = %s", (predicted_name,))
	print(predicted_name)
	data = cur.fetchall()
	mysql.connection.commit()		
	return render_template("index.html", value=data)
											
if __name__ == '__main__':
    app.run()																		# IMG4899.JPG
