import requests
import sqlite3
from datetime import datetime, timedelta
import json
import time
import os

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
STACKEXCHANGE_DB = os.path.join(BASE_DIR, 'stackexchange.db')
BASEURL = "https://api.stackexchange.com/2.2"
KEY = ""
tags = [
	{"site" : "stackoverflow.com", "tag" : "python"},
	{"site" : "stackoverflow.com", "tag" : "javascript"},
]

def connect_db():
	return sqlite3.connect(STACKEXCHANGE_DB)

db = connect_db()

MAX_RETRIES = 20
count = 0

s = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
s.mount('https://', adapter)
s.mount('http://', adapter)

print("Starting.")
for tag in tags:
	compare_date = datetime.now() - timedelta(days=1)
	params = {
	  "site" : tag['site'],
	  "tagged" : tag['tag'],
	  "key" : KEY,
	  "pagesize": 100,
	  "max": int(compare_date.timestamp())
	}
	r = s.get(BASEURL + "/questions", params=params)
	print("+1 Request")
	ids = []

	if r.text:
		all_questions_json = json.loads(r.text)
	else:
		all_questions_json = {}

	if "items" in all_questions_json and len(all_questions_json["items"]) > 0:
		for i in all_questions_json["items"]:
			if i['answer_count'] < 1 and "closed_date" not in i:
				ids.append(str(i["question_id"]))
		r1 = s.get(BASEURL + "/questions/" + ";".join(ids) + "/comments", params={"site" : tag['site'], "key" : KEY, "pagesize": 100})
		print("+1 Request")

		if r1.text:
			comments = json.loads(r1.text)
		else:
			comments = {}

		if "items" in comments and len(comments['items']) > 0:
			for comment in comments['items']:
				for id in ids:
					if str(comment['post_id']) == id:
						ids.remove(id)
		else:
			print("No comments found.")
	else:
		print("No questions found.")

	if len(ids) > 0:
		for id in ids:
			question = [q for q in all_questions_json['items'] if str(q['question_id']) == id][0]
			cur = db.execute('select * from questions WHERE question_id = ?', [question['question_id']])
			questions = cur.fetchall()
			if (len(questions) < 1):
				tags = question['tags']
				tags_str = ",".join(tags)
				db.execute('INSERT INTO questions (question_id, site, tag, link, title, date, tags) VALUES (?, ?, ?, ?, ?, ?, ?)', [question['question_id'], str(tag['site']), str(tag['tag']), question['link'], str(question["title"]), question['creation_date'], tags_str])
				db.commit()
				count += 1
		print("Questions have been saved to database.")
	else:
		print("This tag has no results.")

db.execute("INSERT INTO question_log (message, date) VALUES (?, DATETIME('now'))", ["+" + str(count) + " questions have been added."])
db.commit()

print("Finished.")