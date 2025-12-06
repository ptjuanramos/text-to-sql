CREATE TABLE promotions
(
   promo_id               NUMBER(6)      NOT NULL,
   promo_name             VARCHAR2(30)   NOT NULL,
   promo_subcategory      VARCHAR2(30)   NOT NULL,
   promo_subcategory_id   NUMBER         NOT NULL,
   promo_category         VARCHAR2(30)   NOT NULL,
   promo_category_id      NUMBER         NOT NULL,
   promo_cost             NUMBER(10,2)   NOT NULL,
   promo_begin_date       DATE           NOT NULL,
   promo_end_date         DATE           NOT NULL,
   promo_total            VARCHAR2(15)   NOT NULL,
   promo_total_id         NUMBER         NOT NULL,
   CONSTRAINT promo_pk
      PRIMARY KEY (promo_id)
);
