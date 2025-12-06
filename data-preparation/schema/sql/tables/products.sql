CREATE TABLE products
(
   prod_id                 NUMBER(6)        NOT NULL,
   prod_name               VARCHAR2(50)     NOT NULL,
   prod_desc               VARCHAR2(4000)   NOT NULL,
   prod_subcategory        VARCHAR2(50)     NOT NULL,
   prod_subcategory_id     NUMBER           NOT NULL,
   prod_subcategory_desc   VARCHAR2(2000)   NOT NULL,
   prod_category           VARCHAR2(50)     NOT NULL,
   prod_category_id        NUMBER           NOT NULL,
   prod_category_desc      VARCHAR2(2000)   NOT NULL,
   prod_weight_class       NUMBER(3)        NOT NULL,
   prod_unit_of_measure    VARCHAR2(20),
   prod_pack_size          VARCHAR2(30)     NOT NULL,
   supplier_id             NUMBER(6)        NOT NULL,
   prod_status             VARCHAR2(20)     NOT NULL,
   prod_list_price         NUMBER(8,2)      NOT NULL,
   prod_min_price          NUMBER(8,2)      NOT NULL,
   prod_total              VARCHAR2(13)     NOT NULL,
   prod_total_id           NUMBER           NOT NULL,
   prod_src_id             NUMBER,
   prod_eff_from           DATE,
   prod_eff_to             DATE,
   prod_valid              VARCHAR2(1),
   CONSTRAINT products_pk
      PRIMARY KEY (prod_id)
);
