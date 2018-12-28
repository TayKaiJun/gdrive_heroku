# Connecting Dialogflow with Python

This project allows you pull data from queries received by Dialogflow, and execute the Python scripts needed to process those data by deploying this project on Heroku.

## Important Note

Keep up the practise of commenting and documenting as much as possible for 2 reasons:
* For continuity, since other collaborators will now be able to use this code with ease.
* To help yourself keep track of what the code is doing, so that when the project expands and the code gets longer and more complex, you won't be lost and waste a lot of time debugging.
* Because I have already put in a lot of effort doing it so please help me see it through :')
*For editing this README doc, you can refer to this [website](https://help.github.com/articles/basic-writing-and-formatting-syntax/)*

Also, do check on some basic functions of git so that you know what you are doing when branching/pulling/pushing/fetching/committing/etc. so that you won't make mistakes accidentally.

Lastly, happy coding! :D

## Direction of Use

The following will briefly describe the role of each file in this project for you to get an understanding of what documents need to be updated whenever changes are made. Do try your best to update this README doc if new files are added or the file structure of the project is changed.

### lib/open

Contains the Vokaturi libraries. These libraries are called by this line:

```
Vokaturi.load("lib/open/linux/OpenVokaturi-3-0-linux64.so")
```

*(Note that Heroku engines are Linux based so we need to load the Linux library instead of Windows)*

### Procfile

Not entirely sure how this file is used, but my guess is that it will use the gunicorn library to launch the web app. What is important to note for now is that the "main:app:"

```
web: gunicorn main:app --log-file -
```
refers to the following "app" object in the "main.py" file

```
app = Flask(__name__)
```

So, if the python file name is to be changed or "app" is renamed, be sure to update the Procfile accordingly or there will be error.

### requirements.txt

This file will be used by the Heroku engine to identify which libraries are needed to be pip installed. 
(For example, if we need the "deepaffects" package on our computers, we will use "pip install". But instead, to run it on Heroku, add "deepaffects" to the list in this file instead)

### runtime.txt

Again, not entirely sure how this file is used, but my guess is that it will tell the Heroku engine which environment to build the project in. Hence, the current code:

```
python-3.7.1
```

Will tell Heroku to run our python project with Python 3.7.1
Update this file if newer versions of Python are realeased should you wish to use the latest version of Python.

### main.py

This file contains the main logic used to do everything. Comments have been used to explain what portions of the code do. It will be ideal to continue commenting and documenting as much as possible.

### .json Files

Currently, these JSON files contains the credentials needed for the Google APIs to work. Becareful to update the names of the files in the "main.py" code should these files be renamed, otherwise there will be errors.

Example:
```
credentials = ServiceAccountCredentials.from_json_keyfile_name("gsheet_credentials.json", scope)
```

