CREATE TABLE Debs(
	id	SERIAL8 PRIMARY KEY,
	stat TEXT,
	name TEXT,
	version TEXT,
	architecture TEXT
);

CREATE TABLE Flavor(
	id SERIAL8 PRIMARY KEY,
	flavors TEXT
);

CREATE TABLE Ansible(
	id SERIAL8 PRIMARY KEY,
	scanned_files TEXT
);