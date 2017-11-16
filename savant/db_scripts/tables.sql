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

CREATE TABLE IF NOT EXISTS Scan(
    id SERIAL8 PRIMARY KEY,
    scan_timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ScanDebs(
    id SERIAL8 PRIMARY KEY,
    debs_id INT REFERENCES Debs (id),
    scan_timestamp_id INT REFERENCES Scan (id)
);

CREATE TABLE IF NOT EXISTS ScanGroups(
    id SERIAL8 PRIMARY KEY,
    groups_id INT REFERENCES Groups (id),
    scan_timestamp_id INT REFERENCES Scan (id)
);

CREATE TABLE IF NOT EXISTS ScanShadow(
    id SERIAL8 PRIMARY KEY,
    shadow_id INT REFERENCES Shadow (id),
    scan_timestamp_id INT REFERENCES Scan (id)
);

CREATE TABLE IF NOT EXISTS ScanUsers(
    id SERIAL8 PRIMARY KEY,
    users_id INT REFERENCES Users (id),
    scan_timestamp_id INT REFERENCES Scan (id)
);

CREATE TABLE IF NOT EXISTS Knowledge(
    id SERIAL8 PRIMARY KEY,
    name TEXT,
    resource TEXT,
    action TEXT
);

CREATE TABLE IF NOT EXISTS KnowledgeDebs(
    id SERIAL8 PRIMARY KEY,
    debs_id INT REFERENCES Debs (id),
    knowledge_id INT REFERENCES Knowledge (id)
);

CREATE TABLE IF NOT EXISTS KnowledgeGroups(
    id SERIAL8 PRIMARY KEY,
    groups_id INT REFERENCES Groups (id),
    knowledge_id INT REFERENCES Knowledge (id)
);

CREATE TABLE IF NOT EXISTS KnowledgeShadow(
    id SERIAL8 PRIMARY KEY,
    shadow_id INT REFERENCES Shadow (id),
    knowledge_id INT REFERENCES Knowledge (id)
);

CREATE TABLE IF NOT EXISTS KnowledgeUsers(
    id SERIAL8 PRIMARY KEY,
    users_id INT REFERENCES Users (id),
    knowledge_id INT REFERENCES Knowledge (id)
);