#!/usr/bin/python

import os
import time
import itertools
import psycopg2
from subprocess import call
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from datetime import datetime, timedelta

dbuser = os.environ["DB_USER"]
dbhost = os.environ["DB_HOST"]
dbname = os.environ["DB_NAME"]
dbpass = os.environ["DB_PASS"]
dbtable = os.environ["DB_TABLE"]

params ="host=%s dbname=%s user=%s password=%s" % (dbhost, dbname, dbuser, dbpass)

def delete_data(data):
  try:
    conn = psycopg2.connect(params)
    cursor = conn.cursor()
    query = """DELETE FROM EVENTS WHERE EVENTS_ID = %s"""
    for line in data:
      cursor.execute(query,[line['events_id']])
    conn.commit()
    cursor.close()
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)
  else:
    print "data removed from database"
  finally:
    conn.close()

def send_data(filename):
  try:
    aws_connection = S3Connection(os.environ["AWS_KEY"], os.environ["AWS_SECRET"])
    bucket = aws_connection.get_bucket('admssa')
    bkt = Key(bucket)
    bkt.key = dbtable + filename
    bkt.set_contents_from_filename(filename)
  except Exception:
    print "S3 connection error"
  else:
    print "data sended"
    result = 1
  finally:
    aws_connection.close()
  return result


def get_data():
  try:
    conn = psycopg2.connect(params)
    cursor = conn.cursor()

    query = """SELECT * FROM EVENTS WHERE EVENT_DATE >= %s"""
    date = datetime.now() - timedelta(days=7)
    cursor.execute(query,[date])
    desc = cursor.description
    column_names = [col[0] for col in desc]
    data = [dict(itertools.izip(column_names, row))
        for row in cursor.fetchall()]
    filename= str(date.date()) + ".data"
    file = open(filename, 'w')
    for line in data:
      file.write(str(line)+"\n")
    file.close()
    cursor.close()
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)
  finally:
    conn.close()
  if send_data(filename):
    delete_data(data)

get_data()


