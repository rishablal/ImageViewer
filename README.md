# ImageViewer

### Description: ###
This is a basic web application in Flask, which accepts image files to be uploaded to an Amazon S3 Bucket, and then 
displayed on the browser to view.

This application is currently deployed on Heroku, found [here](https://plain-old-image-viewer.herokuapp.com/).

### Setup: ###
1. Install python https://www.python.org/downloads/
2. Clone this repo
3. Go into root dir of repo
4. Create Virtual Env
	1. ```bash 
		> python -m venv venv
		```
5. Activate Virtual Env (only need to do once per shell session, to deactivate type the word deactivate)
	1. ```bash
		> cd venv/bin
		> source activate
		```
6. cd to root of repo
7. Install Dependencies
	1. ```bash
		> pip3 install -r requirements.txt
		```
8. Create an Amazon S3 bucket and add the following credentials to config.py (DO NOT COMMIT THESE, THEY ARE SECRET):
    1. AWS_ACCESS_KEY_ID
    2. AWS_SECRET_ACCESS_KEY
    3. S3_LOCATION
  
### Run Server Locally: ###
1. cd to repo
2. Activate Virtual Env (only need to do once per shell session, to deactivate type the word deactivate)
	1. ```bash
		> cd venv/bin
		> source activate
		```
3. Go back to root of repo
4. Set Flask Env (only need to do once per shell session, will need to repeat if you restarted the shell)
	1. Windows
		1. ```bash
			> set FLASK_ENV=development
			> set FLASK_APP=api/routes.py
			```
	2. Linux/Mac
		1. ```bash
			> export FLASK_ENV=development
			> export FLASK_APP=api/routes.py
			```
5. ```bash
	> flask run
	```
	or
6. ```bash
	> python run.py
	```
	1. You should see the server run on localhost:5000
