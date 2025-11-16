CREATE TABLE costs
(
   prod_id      NUMBER         NOT NULL,
   time_id      DATE           NOT NULL,
   promo_id     NUMBER         NOT NULL,
   channel_id   NUMBER         NOT NULL,
   unit_cost    NUMBER(10,2)   NOT NULL,
   unit_price   NUMBER(10,2)   NOT NULL,
   CONSTRAINT costs_promo_fk
      FOREIGN KEY (promo_id)   REFERENCES promotions (promo_id),
   CONSTRAINT costs_product_fk
      FOREIGN KEY (prod_id)    REFERENCES products (prod_id),
   CONSTRAINT costs_time_fk
      FOREIGN KEY (time_id)    REFERENCES times (time_id),
   CONSTRAINT costs_channel_fk
      FOREIGN KEY (channel_id) REFERENCES channels (channel_id)
)
