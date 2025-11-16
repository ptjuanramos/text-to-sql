CREATE TABLE countries
(
   country_id             NUMBER         NOT NULL,
   country_iso_code       CHAR(2)        NOT NULL,
   country_name           VARCHAR2(40)   NOT NULL,
   country_subregion      VARCHAR2(30)   NOT NULL,
   country_subregion_id   NUMBER         NOT NULL,
   country_region         VARCHAR2(20)   NOT NULL,
   country_region_id      NUMBER         NOT NULL,
   country_total          VARCHAR2(11)   NOT NULL,
   country_total_id       NUMBER         NOT NULL,
   CONSTRAINT countries_pk
      PRIMARY KEY (country_id)
);
