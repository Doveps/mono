-- Storing Functions --

CREATE OR REPLACE FUNCTION store_debs(in par_stat TEXT, in par_name TEXT, in par_version TEXT, in par_arch TEXT)
 RETURNS TEXT AS
$$
DECLARE
  loc_res  TEXT;
BEGIN

  INSERT INTO Debs(stat, name, version, architecture) VALUES (par_stat, par_name, par_version, par_arch);
  loc_res = 'OK';
  return loc_res;
END;
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION store_groups(in par_group_name TEXT, in par_password TEXT, in par_gid TEXT, in par_users TEXT)
 RETURNS TEXT AS
$$
DECLARE
  loc_res  TEXT;
BEGIN

  INSERT INTO Groups(group_name, password, gid, users) VALUES (par_group_name, par_password, par_gid, par_users);
  loc_res = 'OK';
  return loc_res;
END;
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION store_shadow(in par_username TEXT, in par_password TEXT, in par_lastchanged TEXT,
 in par_min TEXT, in par_max TEXT, in par_warn TEXT, in par_inactive TEXT, in par_expire TEXT, in par_reserve TEXT)
 RETURNS TEXT AS
$$
DECLARE
  loc_res  TEXT;
BEGIN

  INSERT INTO Shadow(username, password, lastchanged, minimum, maximum, warn, inactive, expire, reserve)
   VALUES (par_username, par_password, par_lastchanged, par_min, par_max, par_warn, par_inactive, par_expire, par_reserve);
  loc_res = 'OK';
  return loc_res;
END;
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION store_users(in par_username TEXT, in par_password TEXT, in par_uid TEXT, in par_gid TEXT,
 in par_description TEXT, in par_user_path TEXT, in par_shell TEXT)
 RETURNS TEXT AS
$$
DECLARE
  loc_res  TEXT;
BEGIN

  INSERT INTO Users(username, password, uid, gid, description, user_path, shell)
   VALUES (par_username, par_password, par_uid, par_gid, par_description, par_user_path, par_shell);
  loc_res = 'OK';
  return loc_res;
END;
$$
LANGUAGE 'plpgsql';



-- Get Functions --

CREATE OR REPLACE FUNCTION get_debs(OUT BIGINT, OUT TEXT, OUT TEXT, OUT TEXT, OUT TEXT)
 RETURNS SETOF RECORD AS
$$
	SELECT id, stat, name, version, architecture
	FROM Debs;
$$
LANGUAGE 'sql';

CREATE OR REPLACE FUNCTION get_groups(OUT BIGINT, OUT TEXT, OUT TEXT, OUT TEXT, OUT TEXT)
 RETURNS SETOF RECORD AS
$$
  SELECT id, group_name, password, gid, users
  FROM Groups;
$$
LANGUAGE 'sql';

CREATE OR REPLACE FUNCTION get_shadow(OUT BIGINT, OUT TEXT, OUT TEXT, OUT TEXT, OUT TEXT, OUT TEXT, OUT TEXT, OUT TEXT, OUT TEXT, OUT TEXT)
 RETURNS SETOF RECORD AS
$$
  SELECT id, username, password, lastchanged, minimum, maximum, warn, inactive, expire, reserve
  FROM Shadow;
$$
LANGUAGE 'sql';

CREATE OR REPLACE FUNCTION get_users(OUT BIGINT, OUT TEXT, OUT TEXT, OUT TEXT, OUT TEXT, OUT TEXT, OUT TEXT, OUT TEXT)
 RETURNS SETOF RECORD AS
$$
  SELECT id, username, password, uid, gid, description, user_path, shell
  FROM Users;
$$
LANGUAGE 'sql';

-- Check Duplicates --

CREATE OR REPLACE FUNCTION deb_exists(in par_stat TEXT, in par_name TEXT, in par_version TEXT, in par_arch TEXT) 
  RETURNS TEXT AS
  $$

    DECLARE response TEXT;

    BEGIN
      IF EXISTS(SELECT 1 FROM Debs WHERE stat=par_stat AND name=par_name AND version=par_version AND architecture=par_arch) THEN 
        response := 'TRUE';
      ELSE
        response := 'FALSE';
      END IF;

      RETURN response;
      
    END
  $$    
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION group_exists(in par_group_name TEXT, in par_password TEXT, in par_gid TEXT, in par_users TEXT) 
  RETURNS TEXT AS
  $$

    DECLARE response TEXT;

    BEGIN
      IF EXISTS(SELECT 1 FROM Groups WHERE group_name=par_group_name AND password=par_password AND gid=par_gid AND users=par_users) THEN 
        response := 'TRUE';
      ELSE
        response := 'FALSE';
      END IF;

      RETURN response;
      
    END
  $$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION shadow_exists(in par_username TEXT, in par_password TEXT, in par_lastchanged TEXT,
 in par_min TEXT, in par_max TEXT, in par_warn TEXT, in par_inactive TEXT, in par_expire TEXT, in par_reserve TEXT) 
  RETURNS TEXT AS
  $$

    DECLARE response TEXT;

    BEGIN
      IF EXISTS(SELECT 1 FROM Shadow WHERE username=par_username AND password=par_password AND lastchanged=par_lastchanged AND
       minimum=par_min AND maximum=par_max AND warn=par_warn AND inactive=par_inactive AND expire=par_expire AND reserve=par_reserve) THEN 
        response := 'TRUE';
      ELSE
        response := 'FALSE';
      END IF;

      RETURN response;
      
    END
  $$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION user_exists(in par_username TEXT, in par_password TEXT, in par_uid TEXT, in par_gid TEXT,
 in par_description TEXT, in par_user_path TEXT, in par_shell TEXT) 
  RETURNS TEXT AS
  $$

    DECLARE response TEXT;

    BEGIN
      IF EXISTS(SELECT 1 FROM Users WHERE username=par_username AND password=par_password AND uid=par_uid AND gid=par_gid AND
        description=par_description AND user_path=par_user_path AND shell=par_shell) THEN 
        response := 'TRUE';
      ELSE
        response := 'FALSE';
      END IF;

      RETURN response;
      
    END
  $$
LANGUAGE 'plpgsql';

-- ID Getter Functions --

CREATE OR REPLACE FUNCTION get_debs_id(in par_name TEXT)
 RETURNS BIGINT AS
$$
    SELECT id
    FROM Debs
     WHERE
        name=par_name;
$$
LANGUAGE 'sql';

CREATE OR REPLACE FUNCTION get_groups_id(in par_group_name TEXT)
 RETURNS BIGINT AS
$$
    SELECT id
    FROM Groups
     WHERE
        group_name=par_group_name;
$$
LANGUAGE 'sql';

CREATE OR REPLACE FUNCTION get_shadow_id(in par_username TEXT)
 RETURNS BIGINT AS
$$
    SELECT id
    FROM Shadow
     WHERE
        username=par_username;
$$
LANGUAGE 'sql';

CREATE OR REPLACE FUNCTION get_users_id(in par_username TEXT)
 RETURNS BIGINT AS
$$
    SELECT id
    FROM Users
     WHERE
        username=par_username;
$$
LANGUAGE 'sql';