CREATE MATERIALIZED VIEW fweek_pscat_sales_mv
--  ON PREBUILT TABLE
   ENABLE QUERY REWRITE
   AS
   SELECT   t.week_ending_day,
            p.prod_subcategory,
            SUM(s.amount_sold) AS dollars,
            s.channel_id,
            s.promo_id
   FROM     sh.sales s,
            sh.times t,
            sh.products p
   WHERE    s.time_id = t.time_id
      AND   s.prod_id = p.prod_id
   GROUP BY t.week_ending_day,
            p.prod_subcategory,
            s.channel_id,
            s.promo_id;
