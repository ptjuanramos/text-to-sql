CREATE TABLE channels
(
   channel_id         NUMBER         NOT NULL,
   channel_desc       VARCHAR2(20)   NOT NULL,
   channel_class      VARCHAR2(20)   NOT NULL,
   channel_class_id   NUMBER         NOT NULL,
   channel_total      VARCHAR2(13)   NOT NULL,
   channel_total_id   NUMBER         NOT NULL,
   CONSTRAINT channels_pk
      PRIMARY KEY (channel_id)
);