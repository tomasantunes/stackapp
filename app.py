from flask import Flask, request, g, redirect, url_for, abort, render_template, session, jsonify
import json
import sqlite3
import os
from config import *
from flask_session import Session

DEBUG = False
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
STACKEXCHANGE_DB = os.path.join(BASE_DIR, 'stackexchange.db')
SESSION_TYPE = 'redis'

app = Flask(__name__)
app.config.from_object(__name__)
Session(app)
app.secret_key = ""

def connect_stackexchange_db():
	return sqlite3.connect(app.config['STACKEXCHANGE_DB'])

@app.route('/login/<token>', methods=['GET'])
def login(token):
	if token == SECRET_TOKEN:
		session['isLoggedIn'] = True
		return redirect('/')
	else:
		return jsonify({"status": "NOK", "data": "Invalid Authorization."})

@app.route('/get/tags')
def get_tags():
	db = connect_stackexchange_db()
	cur = db.execute('SELECT * FROM tags JOIN sites ON tags.site_id = sites.site_id')
	questions = cur.fetchall()
	return jsonify(questions)

@app.route('/get/sites')
def get_sites():
	db = connect_stackexchange_db()
	cur = db.execute('SELECT * FROM sites')
	questions = cur.fetchall()
	return jsonify(questions)

@app.route('/get/questions')
def get_all_questions():
	db = connect_stackexchange_db()
	cur = db.execute('SELECT * FROM questions')
	questions = cur.fetchall()
	return jsonify(questions)

@app.route('/get/questions-by-tag')
def get_questions_by_tag():
	tag_id = request.args['tag_id']
	site_id = request.args['site_id']
	offset = request.args['offset']
	print(offset)
	db = connect_stackexchange_db()
	cur = db.execute('SELECT questions.question_id, questions.link, questions.title, questions.date, questions.status, questions.tags FROM questions JOIN tags ON questions.tag = tags.tag_title JOIN sites ON questions.site = sites.site_url WHERE tags.tag_id = ? AND sites.site_id = ? ORDER BY status LIMIT 10 OFFSET ?', (tag_id, site_id, offset))
	questions = cur.fetchall()
	cur = db.execute("SELECT COUNT(*) FROM questions JOIN tags ON questions.tag = tags.tag_title JOIN sites ON questions.site = sites.site_url WHERE tags.tag_id = ? AND sites.site_id = ?", (tag_id, site_id))
	count = cur.fetchone()[0]
	result = {
		"count": count,
		"questions": questions
	}
	return jsonify(result)

@app.route('/get/status-count')
def get_status_count():
	db = connect_stackexchange_db()
	cur = db.execute("SELECT COUNT(*) FROM questions WHERE status = 'I can''t do this'")
	cant_count = cur.fetchone()[0]
	cur = db.execute("SELECT COUNT(*) FROM questions WHERE status = 'TODO'")
	todo_count = cur.fetchone()[0]
	result = {
		"cant_count": cant_count,
		"todo_count": todo_count
	}
	return jsonify(result)

@app.route('/get/questions-count')
def get_questions_count():
	db = connect_stackexchange_db()
	cur = db.execute("SELECT COUNT(*) FROM questions")
	questions_count = cur.fetchone()[0]
	result = {
		"questions_count": questions_count
	}
	return jsonify(result)


@app.route('/get/questions-by-site')
def get_questions_by_site():
	site_id = request.args['site_id']
	offset = request.args['offset']
	print(offset)
	db = connect_stackexchange_db()
	cur = db.execute('SELECT questions.question_id, questions.link, questions.title, questions.date, questions.status, questions.tags FROM questions JOIN sites ON questions.site = sites.site_url WHERE sites.site_id = ? ORDER BY status LIMIT 10 OFFSET ?', (site_id, offset))
	questions = cur.fetchall()
	cur = db.execute("SELECT COUNT(*) FROM questions JOIN sites ON questions.site = sites.site_url WHERE sites.site_id = ?", (site_id,))
	count = cur.fetchone()[0]
	result = {
		"count": count,
		"questions": questions
	}
	return jsonify(result)

@app.route('/get/stats')
def get_stats():
	db = connect_stackexchange_db()
	cur = db.execute('SELECT COUNT(*) FROM questions')
	total_questions = cur.fetchone()[0]
	return jsonify({"total_questions": total_questions})

@app.route("/update-question-status")
def update_question_status():
	if not session.get('isLoggedIn'):
		return jsonify({"status": "NOK", "data": "Invalid Authorization."})

	id = request.args.get("id")
	status = request.args.get("newStatus")
	db = connect_stackexchange_db()
	cur = db.execute('UPDATE questions SET status = ? WHERE question_id = ?', (status, id))
	db.commit()
	db.close()
	return "OK"

@app.route('/')
def home():
	return render_template('questions.html')
	
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)
