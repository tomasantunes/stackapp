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

sites = list(set([tag['site'] for tag in tags]))

for site in sites:
	cursor.execute("INSERT INTO sites (site_url) VALUES (?)", (site,))

for tag in tags:
	site_id = getSiteId(tag['site'])
	cursor.execute("INSERT INTO tags (site_id, tag_title) VALUES (?, ?)", (site_id, tag['tag']))

conn.commit()
conn.close()

