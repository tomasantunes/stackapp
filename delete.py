import requests
import sqlite3
from datetime import datetime, timedelta

BASE_DIR = '/path/to/dir/'
STACKEXCHANGE_DB = BASE_DIR + 'stackexchange.db'
BASEURL = "https://api.stackexchange.com/2.2/questions"
KEY = ""

def connect_db():
	return sqlite3.connect(STACKEXCHANGE_DB)

db = connect_db()

def chunks(lst, n):
	for i in range(0, len(lst), n):
		yield lst[i:i + n]

print("Starting.")
cur = db.execute('SELECT question_id, site FROM questions')
questions = cur.fetchall()
questions_to_delete = []
questions_obj = {}
compare_date = datetime.now() - timedelta(days=1)

for q in questions:
	if q[1] not in questions_obj.keys():
		questions_obj[q[1]] = []

	questions_obj[q[1]].append(str(q[0]))

for k in questions_obj.keys():
	ids = list(chunks(questions_obj[k], 99))
	for i in ids:
		r1 = requests.get(BASEURL + "/" + ";".join(i) + "/comments", params={"site": k, "key" : KEY, "pagesize": 100})
		comments = r1.json()
		print("+1 Request")

		r2 = requests.get(BASEURL + "/" + ";".join(i), params={"site": k, "key": KEY, "pagesize": 100})
		questions = r2.json()
		print("+1 Request")

		if "items" in comments and len(comments['items']) > 0:
			print("Found comments")
			for c in comments['items']:
				for id in i:
					if str(c['post_id']) == id:
						if id not in questions_to_delete:
							questions_to_delete.append(id)
		else:
			print("No comments found.")


		if "items" in questions and len(questions) > 0:
			print("Found questions")
			for q in questions["items"]:
				if "closed_date" in q or q['answer_count'] > 0 or q["creation_date"] > int(compare_date.timestamp()):
					if str(q["question_id"]) not in questions_to_delete:
						questions_to_delete.append(str(q["question_id"]))
		else:
			print("No questions found")

for q in questions_to_delete:
	db.execute('DELETE FROM questions WHERE question_id = ?', [q])
	db.commit()
	print("Question deleted.")

print("Finished.")
