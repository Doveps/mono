CREATE TABLE IF NOT EXISTS Debs(
	id	SERIAL8 PRIMARY KEY,
	stat TEXT,
	name TEXT,
	version TEXT,
	architecture TEXT
);

CREATE TABLE IF NOT EXISTS Groups(
	id	SERIAL8 PRIMARY KEY,
	group_name TEXT,
	password TEXT,
	gid TEXT,
	users TEXT
);

CREATE TABLE IF NOT EXISTS Shadow(
	id	SERIAL8 PRIMARY KEY,
	username TEXT,
	password TEXT,
	lastchanged TEXT,
	minimum TEXT,
	maximum TEXT,
	warn TEXT,
	inactive TEXT,
	expire TEXT,
	reserve TEXT
);

CREATE TABLE IF NOT EXISTS Users(
	id	SERIAL8 PRIMARY KEY,
	username TEXT,
	password TEXT,
	uid TEXT,
	gid TEXT,
	description TEXT,
	user_path TEXT,
	shell TEXT
);
