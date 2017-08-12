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

