python ./Django/manage.py dumpdata --traceback --natural-foreign --exclude users.profile  --exclude auth.permission --exclude contenttypes --indent 4 > ./Django/dump.json
