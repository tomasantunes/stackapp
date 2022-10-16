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

@app.route('/get/questions')
def get_all_questions():
	db = connect_stackexchange_db()
	cur = db.execute('SELECT * FROM questions')
	questions = cur.fetchall()
	return jsonify(questions)

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
