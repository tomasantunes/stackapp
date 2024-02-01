CREATE TABLE questions(
    question_id INTEGER,
    site TEXT NOT NULL,
    tag TEXT,
    link text NOT NULL,
    title text NOT NULL,
    date date
);

CREATE TABLE sites(
    site_id INTEGER PRIMARY KEY AUTOINCREMENT,
    site_url TEXT
);

CREATE TABLE tags(
    tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
    site_id INTEGER NOT NULL,
    tag_title TEXT
);

CREATE TABLE question_log(
    message TEXT,
    date TEXT
);

ALTER TABLE questions ADD COLUMN status TEXT;
ALTER TABLE questions ADD COLUMN tags TEXT;