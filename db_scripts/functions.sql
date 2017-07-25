CREATE OR REPLACE FUNCTION store_import (par_import TEXT) RETURNS TEXT AS 
$$
	
	DECLARE
		loc_import TEXT;
		loc_res TEXT;

	BEGIN

		SELECT INTO loc_import Imports 
		FROM Imports
		WHERE Imports = par_import;

		IF loc_import ISNULL
			THEN
				INSERT INTO Import (Imports) VALUES (par_import);
				loc_res = "OK";
		ELSE
			loc_res = "EXISTS";

		END IF;

		RETURN loc_res;
	END;
$$
LANGUAGE 'plpgsql'; 


CREATE OR REPLACE FUNCTION store_flavor (par_flavor TEXT) RETURNS TEXT AS 
$$
	
	DECLARE
		loc_flavor TEXT;
		loc_res TEXT;

	BEGIN

		SELECT INTO loc_flavor Flavors 
		FROM Flavor
		WHERE Flavors = par_flavor;

		IF loc_flavor ISNULL
			THEN
				INSERT INTO Flavor (Flavors) VALUES (par_flavor);
				loc_res = "OK";
		ELSE
			loc_res = "EXISTS";

		END IF;

		RETURN loc_res;
	END;
$$
LANGUAGE 'plpgsql'; 

CREATE OR REPLACE FUNCTION store_ansible_files (par_scanned TEXT) RETURNS TEXT AS 
$$
	
	DECLARE
		loc_scanned TEXT;
		loc_res TEXT;

	BEGIN

		SELECT INTO loc_scanned Scanned_Files 
		FROM Ansible
		WHERE Scanned_Files = par_scanned;

		IF loc_scanned ISNULL
			THEN
				INSERT INTO Ansible (Scanned_Files) VALUES (par_scanned);
				loc_res = "OK";
		ELSE
			loc_res = "EXISTS";

		END IF;

		RETURN loc_res;
	END;
$$
LANGUAGE 'plpgsql'; 
