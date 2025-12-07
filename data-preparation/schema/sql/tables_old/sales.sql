CREATE TABLE sales
(
   prod_id         NUMBER(6)      NOT NULL,
   cust_id         NUMBER         NOT NULL,
   time_id         DATE           NOT NULL,
   channel_id      NUMBER(1)      NOT NULL,
   promo_id        NUMBER(6)      NOT NULL,
   quantity_sold   NUMBER(3)      NOT NULL,
   amount_sold     NUMBER(10,2)   NOT NULL,
   CONSTRAINT sales_promo_fk
      FOREIGN KEY (promo_id)   REFERENCES promotions (promo_id),
   CONSTRAINT sales_customer_fk
      FOREIGN KEY (cust_id)    REFERENCES customers (cust_id),
   CONSTRAINT sales_product_fk
      FOREIGN KEY (prod_id)    REFERENCES products (prod_id),
   CONSTRAINT sales_channel_fk
      FOREIGN KEY (channel_id) REFERENCES channels (channel_id),
   CONSTRAINT sales_time_fk
      FOREIGN KEY (time_id) REFERENCES times (time_id)
)