
/* 
ESTO TENEIS QUE HACERLO MANUALMENTE
sudo subl /etc/postgresql/11/main/pg_hba.conf:90
Cambiamos
local   all      all	   peer
Por
local   all      all	   md5
*/

DROP TABLE IF EXISTS  districtes CASCADE;
DROP TABLE IF EXISTS  barris 	 CASCADE;
DROP TABLE IF EXISTS  wifi 		 CASCADE;
DROP TABLE IF EXISTS  wifi_madre CASCADE;

CREATE TABLE wifi_madre(
    CODI_CAPA 	   VARCHAR(255),
    CAPA_GENERICA  VARCHAR(255),
    NOM_CAPA 	   VARCHAR(255),
    ED50_COORD_X   DECIMAL(11,4),
    ED50_COORD_Y   DECIMAL(11,4),
    ETRS89_COORD_X DECIMAL(11,4),
    ETRS89_COORD_Y DECIMAL(11,4),
    LONGITUD 	   DECIMAL(11,4),
    LATITUD 	   DECIMAL(11,4),
    EQUIPAMENT     VARCHAR(255),
    DISTRICTE      INT,
    BARRI 	   	   INT,
    NOM_DISTRICTE  VARCHAR(255),
    NOM_BARRI      VARCHAR(255),
    ADRECA 		   VARCHAR(255),
    TELEFON    	   VARCHAR(255)
    );    

\COPY wifi_madre (CODI_CAPA,CAPA_GENERICA,NOM_CAPA,ED50_COORD_X,ED50_COORD_Y,ETRS89_COORD_X,ETRS89_COORD_Y,LONGITUD,LATITUD,EQUIPAMENT,DISTRICTE,BARRI,NOM_DISTRICTE,NOM_BARRI,ADRECA,TELEFON) FROM 'PUNTS_WIFI.csv' delimiter ',' csv header;    

CREATE TABLE districtes(
    IdDistricte   INT PRIMARY KEY,
    Nom_Districte VARCHAR(255)
    );
	
CREATE TABLE barris(
    IdBarri     INT PRIMARY KEY, 
    IdDistricte INT,
    Nom_Barri   VARCHAR(255),
	FOREIGN KEY (IdDistricte) REFERENCES districtes (IdDistricte)
    );

CREATE TABLE wifi(
    ID_WIFI 	   INT GENERATED ALWAYS AS IDENTITY,
    ETRS89_COORD_X DECIMAL(11,4),
    ETRS89_COORD_Y DECIMAL(11,4),
    LONGITUD 	   DECIMAL(11,4),
    LATITUD 	   DECIMAL(11,4),
    EQUIPAMENT     VARCHAR(255),
    BARRI 		   INT,
    ADRECA 		   VARCHAR(255),
    TELEFON    	   VARCHAR(255),
	PRIMARY KEY (ID_WIFI),
	FOREIGN KEY (BARRI) REFERENCES barris (IdBarri)
    );    
    
CREATE OR REPLACE PROCEDURE TRASPASO_DATOS ()
LANGUAGE plpgsql
AS $$
DECLARE
		IMPORT_DISTRICTES CURSOR FOR
		SELECT DISTINCT(DISTRICTE),NOM_DISTRICTE
			FROM wifi_madre
			GROUP BY DISTRICTE,NOM_DISTRICTE
			ORDER BY DISTRICTE ASC;
	v_districte    wifi_madre.DISTRICTE%TYPE;
	v_n_districte  wifi_madre.NOM_DISTRICTE%TYPE;

	IMPORT_BARRIS CURSOR FOR
		SELECT DISTINCT(BARRI),NOM_BARRI,DISTRICTE
			FROM wifi_madre
			GROUP BY BARRI,NOM_BARRI,DISTRICTE
			ORDER BY BARRI ASC;
	v_barri     	wifi_madre.BARRI%TYPE;
	v_n_barri   	wifi_madre.NOM_BARRI%TYPE;
	v_id_districte  wifi_madre.DISTRICTE%TYPE;
	
	IMPORT_WIFI CURSOR FOR
		SELECT ETRS89_COORD_X,ETRS89_COORD_Y,
			   LONGITUD,LATITUD,EQUIPAMENT,BARRI,ADRECA,TELEFON
			FROM wifi_madre;
		
	v_etrs89_coordx     wifi_madre.ETRS89_COORD_X%TYPE;
	v_etrs89_coordy     wifi_madre.ETRS89_COORD_Y%TYPE;
	v_long    			wifi_madre.LONGITUD%TYPE;
	v_lat   			wifi_madre.LATITUD%TYPE;
	v_equip    			wifi_madre.EQUIPAMENT%TYPE;
	v_adreca    		wifi_madre.ADRECA%TYPE;
	v_telef    			wifi_madre.TELEFON%TYPE;
	
BEGIN
	OPEN IMPORT_DISTRICTES;
	LOOP
		FETCH IMPORT_DISTRICTES INTO v_districte,v_n_districte;
		IF NOT FOUND THEN 
			EXIT;
		END IF;
		INSERT INTO districtes(IdDistricte,Nom_Districte)
			VALUES (v_districte,v_n_districte);
	END LOOP;
	CLOSE IMPORT_DISTRICTES ;
	COMMIT;

	OPEN IMPORT_BARRIS ;
	LOOP
		FETCH IMPORT_BARRIS  INTO v_barri,v_n_barri,v_id_districte;
		IF NOT FOUND THEN 
			EXIT;
		END IF;
		INSERT INTO barris(IdBarri,Nom_Barri,IdDistricte)
			VALUES (v_barri,v_n_barri,v_id_districte);
	END LOOP;
	CLOSE IMPORT_BARRIS ;
	COMMIT;

	OPEN IMPORT_WIFI ;
	LOOP
		FETCH IMPORT_WIFI  INTO v_etrs89_coordx,v_etrs89_coordy,
								v_long,v_lat,v_equip,v_barri,v_adreca,v_telef;
		IF NOT FOUND THEN 
			EXIT;
		END IF;
		INSERT INTO wifi(ETRS89_COORD_X,ETRS89_COORD_Y,LONGITUD,
						 LATITUD,EQUIPAMENT,BARRI,ADRECA,TELEFON)
			VALUES (v_etrs89_coordx,v_etrs89_coordy,v_long,v_lat,
					v_equip,v_barri,v_adreca,v_telef);
	END LOOP;
	CLOSE IMPORT_WIFI ;
	COMMIT;
END; $$



