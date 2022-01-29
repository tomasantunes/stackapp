from flask import Flask, request, g, redirect, url_for, abort, render_template, session, jsonify
import json
import sqlite3

DEBUG = False
BASE_DIR = '/path/to/dir/'
STACKEXCHANGE_DB = BASE_DIR + 'stackexchange.db'

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = ""

def connect_stackexchange_db():
	return sqlite3.connect(app.config['STACKEXCHANGE_DB'])

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

@app.route('/')
def home():
	return render_template('questions.html')
	
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)
