#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import boto.rds
import os.path, time


AWS_REGION = 'us-east-1'
aws_access_key_id=os.environ["AWS_KEY"]
aws_secret_access_key=os.environ["AWS_SECRET"]
list_files_log='files_list.log'
output='rds.log'
dbinstance_id='ademprod'

conn = boto.rds.connect_to_region(
    AWS_REGION,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key)

if os.path.exists(list_files_log) and os.path.getsize(list_files_log) > 0:
   with open(list_files_log, "rb") as fr:
     last_file_name=fr.readlines()[-1].strip()
else:
   last_file_name=None
with open(output, 'a') as f:
    list_of_files=conn.get_all_logs(dbinstance_id, marker=last_file_name)
    list_of_files.pop()
    with open(list_files_log, 'wb') as fp:
     for item in list_of_files:
            fp.write("%s\n" % item)
     for log_file in list_of_files:
        print 'Download %s(%d)' % (log_file.log_filename,
                                   int(log_file.size))
        try:
            log = conn.get_log_file(dbinstance_id, log_file.log_filename)
            try:
                f.write(log.data)
            except AttributeError:
                pass
        except:
            print 'Error while download %s' % log_file.log_filename
