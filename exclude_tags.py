import sqlite3

BASE_DIR = '/path/to/dir/'
STACKEXCHANGE_DB = BASE_DIR + 'stackexchange.db'

def connect_db():
	return sqlite3.connect(STACKEXCHANGE_DB)

db = connect_db()

section = {"site" : "stackoverflow.com", "tag" : "javascript"}
tags_to_exclude = ["discord.js", "android", "ios"]

print("Starting.")

cur = db.execute('SELECT * FROM questions WHERE site = ? AND tag = ?', (section['site'], section['tag']))
questions = cur.fetchall()

for q in questions:
    if q[7] != None:
        question_tags = q[7].split(",")
        status = "I can't do this"
        for t in question_tags:
            if t in tags_to_exclude:
                db.execute("UPDATE questions SET status = ? WHERE question_id = ?", (status, q[0]))

db.commit()
db.close()

print("Finished.")