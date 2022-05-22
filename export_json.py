import sqlite3
import json
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
STACKEXCHANGE_DB = os.path.join(BASE_DIR, 'stackexchange.db')

def connect_db():
	return sqlite3.connect(STACKEXCHANGE_DB)

db = connect_db()

print("Starting.")
db.row_factory = sqlite3.Row
cur = db.execute('SELECT question_id, site, link, title, date, tags FROM questions')
questions = cur.fetchall()
questions = [dict(row) for row in questions]
  
json_object = json.dumps(questions, indent = 4)
  
with open("questions.json", "w", encoding="utf8") as outfile:
    outfile.write(json_object)

print("Finished.")