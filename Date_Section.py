
#Load Librarys
import pandas as pd
import numpy as np
import psycopg2
import os
import sqlalchemy

#Connect to database
conn = psycopg2.connect(
    host="localhost", 
    database="postgres", #please change database 
    user="postgres", #please change username
    password="123") #please change password

#Create a cursor
conn.autocommit = True
cur = conn.cursor()

#If table exist, Drop Table
query =  "DROP TABLE IF EXISTS date_sequence CASCADE;"
query += "DROP TABLE IF EXISTS date_dim CASCADE;"
cur.execute(query)

#Create date_sequence table
query = "CREATE TABLE date_sequence (date date NOT NULL) \
;"
cur.execute(query)

#Insert Records into date_sequence table
query = "INSERT INTO date_sequence(date) \
SELECT '1960-01-01'::DATE + SEQUENCE.number AS date \
FROM GENERATE_SERIES(0, 27000) AS SEQUENCE (number) \
  ;"
cur.execute(query)

#Create date_dim table
query = "CREATE TABLE date_dim ( \
  date DATE NOT NULL, \
  day_suffix TEXT NOT NULL, \
  day_name TEXT NOT NULL, \
  day_of_week INT NOT NULL, \
  day_of_month INT NOT NULL, \
  day_of_year INT NOT NULL, \
  month INT NOT NULL, \
  month_name TEXT NOT NULL, \
  month_name_abbreviated TEXT NOT NULL, \
  year_value INT NOT NULL, \
  quarter INT NOT NULL, \
  first_day_of_week DATE NOT NULL, \
  last_day_of_week DATE NOT NULL, \
  PRIMARY KEY (date) \
);"
cur.execute(query)

#Insert Records into date_sequence table
query = "INSERT INTO date_dim \
SELECT \
date as date, \
TO_CHAR(date, 'fmDDth') AS day_suffix,  \
TO_CHAR(date, 'TMDay') AS day_name, \
EXTRACT(ISODOW FROM date) AS day_of_week, \
EXTRACT(DAY FROM date) AS day_of_month, \
EXTRACT(DOY FROM date) AS day_of_year,   \
EXTRACT(MONTH FROM date) AS month,   \
TO_CHAR(date, 'TMMonth') AS month_name,   \
TO_CHAR(date, 'Mon') AS month_name_abbreviated,   \
EXTRACT(YEAR FROM date) AS year_value,   \
EXTRACT(quarter FROM date) AS quarter, \
date + (1 - EXTRACT(ISODOW FROM date))::INT AS first_day_of_week,   date + (7 - EXTRACT(ISODOW FROM date))::INT AS last_day_of_week from date_sequence \
ORDER BY date ASC;" \

cur.execute(query)