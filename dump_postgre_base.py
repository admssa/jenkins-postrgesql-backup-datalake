#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import boto
import time
from subprocess import call
from boto.s3.connection import S3Connection
from boto.s3.key import Key

dbpass=os.environ["DB_PASS"]
dbname=os.environ["DB_NAME"]
dbhost=os.environ["DB_HOST"]
dbuser=os.environ["DB_USER"]

date = time.strftime("%d-%m-%Y-%H-%M")

filename= str(date) + ".dump"
file = open(filename, 'w')

os.system("export PGPASSWORD=%s && pg_dump -d %s -h %s -U %s -w -f %s" % (dbpass, dbname, dbhost, dbuser, filename))

try:
  aws_connection = S3Connection(os.environ["AWS_KEY"], os.environ["AWS_SECRET"])
  bucket = aws_connection.get_bucket('admssa')
  bkt = Key(bucket)
  bkt.key = dbname + filename
  bkt.set_contents_from_filename(filename)
except Exception:
    print "S3 connection error"
else:
    print "data saved"
finally:
    aws_connection.close()

