CREATE TABLE IF NOT EXISTS Debs_2(
	id	SERIAL8 PRIMARY KEY,
	stat TEXT,
	name TEXT,
	version TEXT,
	architecture TEXT
);

CREATE OR REPLACE FUNCTION store_debs_2(in par_stat TEXT, in par_name TEXT, in par_version TEXT, in par_arch TEXT)
 RETURNS TEXT AS
$$
DECLARE
  loc_res  TEXT;
BEGIN

  INSERT INTO Debs_2(stat, name, version, architecture) VALUES (par_stat, par_name, par_version, par_arch);
  loc_res = 'OK';
  return loc_res;
END;
$$
LANGUAGE 'plpgsql';
