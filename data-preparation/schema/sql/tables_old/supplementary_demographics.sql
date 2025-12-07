CREATE TABLE supplementary_demographics
(
   cust_id                   NUMBER           NOT NULL,
   education                 VARCHAR2(21),
   occupation                VARCHAR2(21),
   household_size            VARCHAR2(21),
   yrs_residence             NUMBER,
   affinity_card             NUMBER(10),
   cricket                   NUMBER(10),
   baseball                  NUMBER(10),
   tennis                    NUMBER(10),
   soccer                    NUMBER(10),
   golf                      NUMBER(10),
   unknown                   NUMBER(10),
   misc                      NUMBER(10),
   comments                  VARCHAR2(4000),
   CONSTRAINT supp_demo_pk
      PRIMARY KEY (cust_id)
);