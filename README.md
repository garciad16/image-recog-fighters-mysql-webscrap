# image_recog_fighters_mysql_webscrap
image recognition with OpenCv. Fighter's boxing record into database using webscrapping

To run the program:
    -> python3 tester.py

Implementation of the program:

    -> When program runs:
        -> Creates database: 'FightersDB'
            -> Along with two tables: 'Fighters' and 'Fights'. The 'Fighters' table being the parent table and 'Fights' table being the child table
        -> Opens up the HTML version of the database 'FightersDB' with the table 'Fighters' on display. Table contains a list of fighters and their info 
            -> Info is manually typed, not webscrapped 
        -> Top left of the screen is the option to select a face image to be scanned and recognized via OpenCV
            -> When selected:
                -> Program trains the images found in the absolute path directory 
                    -> Program then proceeds to display the image with the name of the person recognized and the confidence level of the image
            -> Program is trained to recognize the image, if not recognized then HTML page will still have the table 'Fighters' on display
            -> If image is recognized then the boxing record of the fighter is scrapped from a website called: https://boxrec.com
                -> The boxing record of the fighter is saved into the database and under the table 'Fights'
            -> While image is on display on the screen, press any keyboard key to close the image window
                -> This will change the HTML page from the table 'Fighters' to 'Fights' with the correct person recognized and their given
                unique fighter_id in the table
                    -> What is now in display is the respective fighter's boxing record and their opponents that is scrapped from https://boxrec.com

Problems with the program:
    -> Image recognition is not accurate, can mistaken the image as someone else 
    -> Only works with one face in the image
    -> Confidence level low sometimes
    -> HTML page needs improvements
