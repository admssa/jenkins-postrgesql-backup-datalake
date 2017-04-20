#!/usr/bin/python

import timestring
import datetime
from boto.s3.connection import S3Connection

AWS_KEY='change it'
AWS_SECRET='change it'
BUCKET='change it'

def remove_old_backups():
  try:
    result = 0
    aws_connection = S3Connection(AWS_KEY, AWS_SECRET)
    bucket = aws_connection.get_bucket(BUCKET)
    month_ago = (datetime.datetime.today() - datetime.timedelta(days=30))
    week_ago = (datetime.datetime.today() - datetime.timedelta(days=7))
    for key in bucket.list():
        modification_date = timestring.Date(key.last_modified)
        if modification_date < month_ago:
            key.delete()
            print 'file ' + key.name + ' was deleted'
        elif modification_date < week_ago and modification_date.weekday != 1:
            key.delete()
            print 'file ' + key.name + ' was deleted'
        else:
            print key.name + ' keeped'
  except Exception:
    print "S3 connection error"
  else:
#    print "connection success"
    result = 1
  finally:
   aws_connection.close()
  return result

remove_old_backups()
