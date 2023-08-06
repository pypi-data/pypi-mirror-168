### patch_for_django_orm
```text
# ===========
# Background:

Django's ORM establishes a database connection per thread.
For the threads managed by Django (which are supposed to be used for directly
handing web requests), Django ORM cleans the established connections up under
the hood once the processing on the thread completes (= request_finished signal).

On the other hand, in the case where Django ORM models are used in an unmanaged thread,
Django does not handle the cleanup of the connections bound to the thread although the
Django framework automatically associates a new connection to the thread. 
This half-maintained resource possibly can cause some DB connection related issues.

To learn more details of this Django behavior, checking the following ticket 
is helpful for understanding this:
https://code.djangoproject.com/ticket/9878

# =========
# Solution:

First replace django orm's mysql database engine by SQLAlchemy connection pool,
Then we need to add put-connection-back-into-pool action when user thread is finished.
To implement above two features in django in a beautiful way, I make this patch. 
If any suggestions, please contact xing.yang@intel.com.
Let's make django more beautiful.

# ===============
# What To Patch ?

patch threading.Thread.
  start
  run
patch django.db.backends.mysql.base.
  Database
  DatabaseWrapper.get_new_connection

# =====
# Usage

# add this in django settings.py to start patch
import ironegg
ironegg.patch_all(pool_size=5, debug=True)
  
# ===============
# Tested versions

python = 3.7/2.7
django = 3.2/1.9
sqlalchemy = 1.4
pymysql = 1.0.2 (python3)
MySQL-python = 1.2.5 (python2)
mysql = 5.7
uwsgi = 2.0

# ====
# Todo

Now this patch is only for mysql database in django,
PostgreSQL and other databases will be supported later.
And only patch threading module in python2/3,
If you use old thread/_thread module to create thread, no patch.
```
