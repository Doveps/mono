CREATE TABLE Import (
	id	SERIAL8 PRIMARY KEY,
	imports TEXT
);

CREATE TABLE Flavor (
	id SERIAL8 PRIMARY KEY,
	flavors TEXT
);

CREATE TABLE Ansible (
	id SERIAL8 PRIMARY KEY,
	scanned_files TEXT
);