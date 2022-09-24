# stackapp
Display questions from Stackexchange

![Stackapp Screeshot 1](https://i.imgur.com/Yw4ds4R.png)
![Stackapp Screeshot 2](https://i.imgur.com/qpwk342.png)

## How to run

- Run this command: pip install flask requests
- Run the init_db.py file to create the database.
- Insert your Stackexchange API key at the KEY variable.
- Change the tags variable in the file questions.py to include the tags you are looking for.
- Run the questions.py file to fetch questions.
- Run the delete.py file to delete questions that already have answers.
- Open the app by running this command: python app.py and then open your browser at localhost:5000
