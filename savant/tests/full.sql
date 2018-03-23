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

CREATE OR REPLACE FUNCTION get_last_scan()
 RETURNS INT AS
 $$
    DECLARE
        timestamp_id INT;
    BEGIN
        SELECT id into timestamp_id from Scan ORDER BY id DESC limit 1;

        RETURN timestamp_id;
    END;
 $$
 LANGUAGE 'plpgsql';

 CREATE OR REPLACE FUNCTION get_last_knowledge()
 RETURNS INT AS
 $$
    DECLARE
        knowledge_id INT;
    BEGIN
        SELECT id into knowledge_id from knowledge ORDER BY id DESC limit 1;

        RETURN knowledge_id;
    END;
 $$
 LANGUAGE 'plpgsql';

-- Storing Functions --

CREATE OR REPLACE FUNCTION store_debs(in par_stat TEXT, in par_name TEXT, in par_version TEXT, in par_arch TEXT)
 RETURNS TEXT AS
$$
DECLARE
  loc_res  TEXT;
  row_id INT;
BEGIN
    IF EXISTS(SELECT 1 FROM Debs WHERE (stat=par_stat OR stat IS NULL) AND (name=par_name OR name IS NULL)
         AND (version=par_version OR version IS NULL) AND (architecture=par_arch OR architecture IS NULL)) THEN

         SELECT id INTO row_id FROM Debs WHERE (stat=par_stat OR stat IS NULL) AND (name=par_name OR name IS NULL)
         AND (version=par_version OR version IS NULL) AND (architecture=par_arch OR architecture IS NULL);
        INSERT INTO ScanDebs(debs_id, scan_timestamp_id) VALUES (row_id, get_last_scan());

    ELSE
        INSERT INTO Debs(stat, name, version, architecture) VALUES (par_stat, par_name, par_version, par_arch);
        SELECT id INTO row_id FROM Debs WHERE (stat=par_stat OR stat IS NULL) AND (name=par_name OR name IS NULL)
         AND (version=par_version OR version IS NULL) AND (architecture=par_arch OR architecture IS NULL);
        INSERT INTO ScanDebs(debs_id, scan_timestamp_id) VALUES (row_id, get_last_scan());
    END IF;

  loc_res = 'OK';
  RETURN loc_res;
END;
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION store_groups(in par_group_name TEXT, in par_password TEXT, in par_gid TEXT, in par_users TEXT)
 RETURNS TEXT AS
$$
DECLARE
  loc_res  TEXT;
  row_id INT;
BEGIN
    IF EXISTS(SELECT 1 FROM Groups WHERE (group_name=par_group_name OR group_name IS NULL) AND (password=par_password OR password IS NULL)
         AND (gid=par_gid OR gid IS NULL) AND (users=par_users OR users IS NULL)) THEN

         SELECT id INTO row_id FROM Groups WHERE (group_name=par_group_name OR group_name IS NULL) AND (password=par_password OR password IS NULL)
         AND (gid=par_gid OR gid IS NULL) AND (users=par_users OR users IS NULL);
        INSERT INTO ScanGroups(groups_id, scan_timestamp_id) VALUES (row_id, get_last_scan());

    ELSE
        INSERT INTO Groups(group_name, password, gid, users) VALUES (par_group_name, par_password, par_gid, par_users);
        SELECT id INTO row_id FROM Groups WHERE (group_name=par_group_name OR group_name IS NULL) AND (password=par_password OR password IS NULL)
         AND (gid=par_gid OR gid IS NULL) AND (users=par_users OR users IS NULL);
        INSERT INTO ScanGroups(groups_id, scan_timestamp_id) VALUES (row_id, get_last_scan());
    END IF;

  loc_res = 'OK';
  RETURN loc_res;
END;
$$ 
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION store_shadow(in par_username TEXT, in par_password TEXT, in par_lastchanged TEXT,
 in par_min TEXT, in par_max TEXT, in par_warn TEXT, in par_inactive TEXT, in par_expire TEXT, in par_reserve TEXT)
 RETURNS TEXT AS
$$
DECLARE
  loc_res  TEXT;
  row_id INT;
BEGIN
    IF EXISTS(SELECT 1 FROM Shadow WHERE (username=par_username OR username IS NULL) AND (password=par_password OR password IS NULL)
         AND (lastchanged=par_lastchanged OR lastchanged IS NULL) AND (minimum=par_min OR minimum IS NULL)
         AND (maximum=par_max OR maximum IS NULL) AND (warn=par_warn OR warn IS NULL) AND (inactive=par_inactive OR inactive IS NULL)
         AND (expire=par_expire OR expire IS NULL) AND (reserve=par_reserve OR reserve IS NULL)) THEN

            SELECT id INTO row_id FROM Shadow WHERE (username=par_username OR username IS NULL) AND (password=par_password OR password IS NULL)
         AND (lastchanged=par_lastchanged OR lastchanged IS NULL) AND (minimum=par_min OR minimum IS NULL)
         AND (maximum=par_max OR maximum IS NULL) AND (warn=par_warn OR warn IS NULL) AND (inactive=par_inactive OR inactive IS NULL)
         AND (expire=par_expire OR expire IS NULL) AND (reserve=par_reserve OR reserve IS NULL);
        INSERT INTO ScanShadow(shadow_id, scan_timestamp_id) VALUES (row_id, get_last_scan());

    ELSE
        INSERT INTO Shadow(username, password, lastchanged, minimum, maximum, warn, inactive, expire, reserve)
        VALUES (par_username, par_password, par_lastchanged, par_min, par_max, par_warn, par_inactive, par_expire, par_reserve);
        SELECT id INTO row_id FROM Shadow WHERE (username=par_username OR username IS NULL) AND (password=par_password OR password IS NULL)
         AND (lastchanged=par_lastchanged OR lastchanged IS NULL) AND (minimum=par_min OR minimum IS NULL)
         AND (maximum=par_max OR maximum IS NULL) AND (warn=par_warn OR warn IS NULL) AND (inactive=par_inactive OR inactive IS NULL)
         AND (expire=par_expire OR expire IS NULL) AND (reserve=par_reserve OR reserve IS NULL);
        INSERT INTO ScanShadow(shadow_id, scan_timestamp_id) VALUES (row_id, get_last_scan());
    END IF;

  loc_res = 'OK';
  RETURN loc_res;
END;
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION store_users(in par_username TEXT, in par_password TEXT, in par_uid TEXT, in par_gid TEXT,
 in par_description TEXT, in par_user_path TEXT, in par_shell TEXT)
 RETURNS TEXT AS
$$
DECLARE
  loc_res  TEXT;
  row_id INT;
BEGIN
    IF EXISTS(SELECT 1 FROM Users WHERE (username=par_username OR username IS NULL) AND (password=par_password OR password IS NULL)
         AND (uid=par_uid OR uid IS NULL) AND (gid=par_gid OR gid IS NULL)
         AND (description=par_description OR description IS NULL) AND (user_path=par_user_path OR user_path IS NULL)
         AND (shell=par_shell OR shell IS NULL)) THEN

            SELECT id INTO row_id FROM Users WHERE (username=par_username OR username IS NULL) AND (password=par_password OR password IS NULL)
         AND (uid=par_uid OR uid IS NULL) AND (gid=par_gid OR gid IS NULL)
         AND (description=par_description OR description IS NULL) AND (user_path=par_user_path OR user_path IS NULL)
         AND (shell=par_shell OR shell IS NULL);
        INSERT INTO ScanUsers(users_id, scan_timestamp_id) VALUES (row_id, get_last_scan());

    ELSE

        INSERT INTO Users(username, password, uid, gid, description, user_path, shell)
        VALUES (par_username, par_password, par_uid, par_gid, par_description, par_user_path, par_shell);
        SELECT id INTO row_id FROM Users WHERE (username=par_username OR username IS NULL) AND (password=par_password OR password IS NULL)
         AND (uid=par_uid OR uid IS NULL) AND (gid=par_gid OR gid IS NULL)
         AND (description=par_description OR description IS NULL) AND (user_path=par_user_path OR user_path IS NULL)
         AND (shell=par_shell OR shell IS NULL);
        INSERT INTO ScanUsers(users_id, scan_timestamp_id) VALUES (row_id, get_last_scan());
    END IF;

  loc_res = 'OK';
  RETURN loc_res;
END;
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION store_datetime()
 RETURNS TEXT AS
$$
DECLARE
  loc_res  TEXT;
BEGIN

  INSERT INTO Scan(scan_timestamp)
   VALUES (current_timestamp);
  loc_res = 'OK';
  RETURN loc_res;
END;
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION store_knowledge(in par_name TEXT, in par_resource TEXT, in par_action TEXT)
 RETURNS TEXT AS
 $$
 DECLARE
    loc_res  TEXT;
BEGIN
    INSERT INTO knowledge(name, resource, action) VALUES (par_name, par_resource, par_action);
    loc_res = 'OK';
    RETURN loc_res;
END;
 $$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION store_knowledge_debs(in par_stat TEXT, in par_name TEXT, in par_version TEXT, in par_arch TEXT)
 RETURNS TEXT AS
 $$
    BEGIN
        INSERT INTO KnowledgeDebs(debs_id, knowledge_id)
         VALUES (get_debs_id(par_stat, par_name, par_version, par_arch), get_last_knowledge());

        RETURN 'OK';
    END;
 $$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION store_knowledge_groups(in par_group_name TEXT, in par_password TEXT, in par_gid TEXT, in par_users TEXT)
 RETURNS TEXT AS
 $$
    BEGIN
        INSERT INTO KnowledgeGroups(groups_id, knowledge_id)
         VALUES (get_groups_id(par_group_name, par_password, par_gid, par_users), get_last_knowledge());

        RETURN 'OK';
    END;
 $$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION store_knowledge_shadow(in par_username TEXT, in par_password TEXT, in par_lastchanged TEXT,
 in par_min TEXT, in par_max TEXT, in par_warn TEXT, in par_inactive TEXT, in par_expire TEXT, in par_reserve TEXT)
 RETURNS TEXT AS
 $$
    BEGIN
        INSERT INTO KnowledgeShadow(shadow_id, knowledge_id)
         VALUES (get_shadow_id(par_username, par_password, par_lastchanged, par_min, par_max, par_warn, par_inactive, par_expire, par_reserve), get_last_knowledge());

        RETURN 'OK';
    END;
 $$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION store_knowledge_users(in par_username TEXT, in par_password TEXT, in par_uid TEXT, in par_gid TEXT,
 in par_description TEXT, in par_user_path TEXT, in par_shell TEXT)
 RETURNS TEXT AS
 $$
    BEGIN
        INSERT INTO KnowledgeUsers(users_id, knowledge_id)
         VALUES (get_users_id(par_username, par_password, par_uid, par_gid, par_description, par_user_path, par_shell), get_last_knowledge());

        RETURN 'OK';
    END;
 $$
LANGUAGE 'plpgsql';
-- Get Functions --

-- Get Unique Data --

CREATE OR REPLACE FUNCTION get_debs_unique(OUT TEXT, OUT TEXT, OUT TEXT, OUT TEXT)
 RETURNS SETOF RECORD AS
$$
    SELECT stat, name, version, architecture FROM Debs INNER JOIN ScanDebs ON Debs.id = ScanDebs.debs_id
    WHERE ScanDebs.scan_timestamp_id = get_last_scan() EXCEPT
     SELECT stat, name, version, architecture FROM Debs INNER JOIN ScanDebs ON Debs.id = ScanDebs.debs_id
     WHERE ScanDebs.scan_timestamp_id = 1;
$$
LANGUAGE 'sql';


CREATE OR REPLACE FUNCTION get_groups_unique(OUT TEXT, OUT TEXT, OUT TEXT, OUT TEXT)
 RETURNS SETOF RECORD AS
$$
 SELECT group_name, password, gid, users FROM Groups INNER JOIN ScanGroups ON Groups.id = ScanGroups.groups_id
    WHERE ScanGroups.scan_timestamp_id = get_last_scan() EXCEPT
     SELECT group_name, password, gid, users FROM Groups INNER JOIN ScanGroups ON Groups.id = ScanGroups.groups_id
     WHERE ScanGroups.scan_timestamp_id = 1;
$$
LANGUAGE 'sql';

CREATE OR REPLACE FUNCTION get_shadow_unique(OUT TEXT, OUT TEXT, OUT TEXT, OUT TEXT, OUT TEXT, OUT TEXT, OUT TEXT, OUT TEXT, OUT TEXT)
 RETURNS SETOF RECORD AS
$$
  SELECT username, password, lastchanged, minimum, maximum, warn, inactive, expire, reserve FROM Shadow INNER JOIN ScanShadow
   ON Shadow.id = ScanShadow.shadow_id WHERE ScanShadow.scan_timestamp_id = get_last_scan()
    EXCEPT
        SELECT username, password, lastchanged, minimum, maximum, warn, inactive, expire, reserve FROM Shadow INNER JOIN ScanShadow
        ON Shadow.id = ScanShadow.shadow_id WHERE ScanShadow.scan_timestamp_id = 1;
$$
LANGUAGE 'sql';


CREATE OR REPLACE FUNCTION get_users_unique(OUT TEXT, OUT TEXT, OUT TEXT, OUT TEXT, OUT TEXT, OUT TEXT, OUT TEXT)
 RETURNS SETOF RECORD AS
$$
  SELECT username, password, uid, gid, description, user_path, shell FROM Users INNER JOIN ScanUsers
   ON Users.id = ScanUsers.users_id WHERE ScanUsers.scan_timestamp_id = get_last_scan()
    EXCEPT
        SELECT username, password, uid, gid, description, user_path, shell FROM Users INNER JOIN ScanUsers
   ON Users.id = ScanUsers.users_id WHERE ScanUsers.scan_timestamp_id = 1;
$$
LANGUAGE 'sql';

----

-- ID Getter Functions --

CREATE OR REPLACE FUNCTION get_debs_id(in par_stat TEXT, in par_name TEXT, in par_version TEXT, in par_arch TEXT)
 RETURNS BIGINT AS
$$
    SELECT id
    FROM Debs
     WHERE
        stat=par_stat AND name=par_name AND version=par_version AND architecture=par_arch;
$$
LANGUAGE 'sql';

CREATE OR REPLACE FUNCTION get_groups_id(in par_group_name TEXT, in par_password TEXT, in par_gid TEXT, in par_users TEXT)
 RETURNS BIGINT AS
$$
    SELECT id
    FROM Groups
     WHERE
        group_name=par_group_name AND password=par_password AND gid=par_gid AND users=par_users;
$$
LANGUAGE 'sql';

CREATE OR REPLACE FUNCTION get_shadow_id(in par_username TEXT, in par_password TEXT, in par_lastchanged TEXT,
 in par_min TEXT, in par_max TEXT, in par_warn TEXT, in par_inactive TEXT, in par_expire TEXT, in par_reserve TEXT)
 RETURNS BIGINT AS
$$
    SELECT id
    FROM Shadow
     WHERE
        username=par_username AND password=par_password AND lastchanged=par_lastchanged AND
       minimum=par_min AND maximum=par_max AND warn=par_warn AND inactive=par_inactive AND expire=par_expire AND reserve=par_reserve;
$$
LANGUAGE 'sql';

CREATE OR REPLACE FUNCTION get_users_id(in par_username TEXT, in par_password TEXT, in par_uid TEXT, in par_gid TEXT,
 in par_description TEXT, in par_user_path TEXT, in par_shell TEXT)
 RETURNS BIGINT AS
$$
    SELECT id
    FROM Users
     WHERE
        username=par_username AND password=par_password AND uid=par_uid AND gid=par_gid AND
        description=par_description AND user_path=par_user_path AND shell=par_shell;
$$
LANGUAGE 'sql';