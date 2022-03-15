import sqlite3
import json

BASE_DIR = '/path/to/dir/'
STACKEXCHANGE_DB = BASE_DIR + 'stackexchange.db'

def connect_db():
	return sqlite3.connect(STACKEXCHANGE_DB)

db = connect_db()

print("Starting.")
cur = db.execute('SELECT link, title FROM questions')
questions = cur.fetchall()
  
json_object = json.dumps(questions, indent = 4)
  
with open("questions.json", "w") as outfile:
    outfile.write(json_object)

print("Finished.")