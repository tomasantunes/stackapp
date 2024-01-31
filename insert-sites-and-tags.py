import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
STACKEXCHANGE_DB = os.path.join(BASE_DIR, 'stackexchange.db')

tags = [
	{"site" : "stackoverflow.com", "tag" : "python"},
	{"site" : "stackoverflow.com", "tag" : "javascript"},
]

conn = sqlite3.connect(STACKEXCHANGE_DB)
cursor = conn.cursor()

def getSiteId(site_url):
	query = cursor.execute("SELECT site_id FROM sites WHERE site_url = ?", (site_url,))
	site_id = query.fetchone()[0]
	return site_id

def checkIfSiteExists(site_url):
	query = cursor.execute("SELECT * FROM sites WHERE site_url = ?", (site_url,))
	res = query.fetchall()
	if (len(res) > 0):
		return True
	return False

def checkIfTagExists(tag_title, site_id):
	query = cursor.execute("SELECT * FROM tags WHERE tag_title = ? AND site_id = ?", (tag_title, site_id))
	res = query.fetchall()
	if (len(res) > 0):
		return True
	return False

sites = list(set([tag['site'] for tag in tags]))

for site in sites:
	if (not checkIfSiteExists(site)):
		cursor.execute("INSERT INTO sites (site_url) VALUES (?)", (site,))

for tag in tags:
	site_id = getSiteId(tag['site'])
	if (not checkIfTagExists(tag['tag'], site_id)):
		cursor.execute("INSERT INTO tags (site_id, tag_title) VALUES (?, ?)", (site_id, tag['tag']))

conn.commit()
conn.close()

