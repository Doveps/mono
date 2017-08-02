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


CREATE OR REPLACE FUNCTION store_flavor(par_flavor TEXT)
  RETURNS TEXT AS
$$
DECLARE
  loc_flavor TEXT;
  loc_res  TEXT;
BEGIN

  SELECT INTO loc_flavor flavors
  FROM Flavor
  WHERE flavors = par_flavor;

  IF loc_import ISNULL
  THEN
    INSERT INTO Flavor (flavors) VALUES (par_flavor);
    loc_res = 'OK';

  ELSE
    loc_res = 'EXISTED';

  END IF;
  RETURN loc_res;
END;
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION store_ansible(par_scanned_files TEXT)
  RETURNS TEXT AS
$$
DECLARE
  loc_ansible TEXT;
  loc_res  TEXT;
BEGIN

  SELECT INTO loc_ansible scanned_files
  FROM Ansible
  WHERE scanned_files = par_scanned_files;

  IF loc_import ISNULL
  THEN
    INSERT INTO Ansible (scanned_files) VALUES (par_scanned_files);
    loc_res = 'OK';

  ELSE
    loc_res = 'EXISTED';

  END IF;
  RETURN loc_res;
END;
$$
LANGUAGE 'plpgsql';

-- Get Functions --
CREATE OR REPLACE FUNCTION get_imports(OUT BIGINT, OUT TEXT)
 RETURNS SETOF RECORD AS
$$
	SELECT id, imports
	FROM import;
$$
LANGUAGE 'sql';

CREATE OR REPLACE FUNCTION get_flavors(OUT BIGINT, OUT TEXT)
 RETURNS SETOF RECORD AS
$$
	SELECT id, flavors
	FROM flavor;
$$
LANGUAGE 'sql';

CREATE OR REPLACE FUNCTION get_ansible_files(OUT BIGINT, OUT TEXT)
 RETURNS SETOF RECORD AS
$$
	SELECT id, scanned_files
	FROM ansible;
$$
LANGUAGE 'sql';