PATCH_EXPLAIN = """
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
"""

import sys
import time
import threading
try:
    # python3 use pymysql replace MySQLdb
    if sys.version_info < (3, 0):
        import MySQLdb
    else:
        import pymysql; pymysql.install_as_MySQLdb()
    from django.db import close_old_connections
    from django.db.backends.mysql import base
    from django.db.backends.mysql.base import DatabaseWrapper
    from sqlalchemy import pool
except Exception:
    raise Exception('import module error\n=> please make sure django & sqlalchemy & MySQLdb or pymysql installed.')


def patch_all(**kw):
    # print(PATCH_EXPLAIN)
    patch_thread(**kw)
    patch_django_mysql_engine(**kw)


def patch_thread(**kw):
    print("=== patch threading.Thread")

    # print conn close log for debug
    DEBUG = kw.get("debug", False)

    # patch threading.Thread to add django.db.close_old_connections after user's Thread.run
    def patch_Thread_run(func):
        def new_run(*args, **kwargs):
            # call user's run first
            result = func(*args, **kwargs)
            # then call close conn
            close_old_connections()
            if DEBUG:
                print("=== close conn in thread: %s" % threading.current_thread().name)
            return result
        return new_run

    def patch_Thread_start(func):
        def new_start(self, *args, **kwargs):
            # patch user's run in Thread.start because 
            # some users like overide Thread.run, so patch start is more reliable
            threading._old_run = self.run
            self.run = patch_Thread_run(threading._old_run)
            return func(self, *args, **kwargs)
        return new_start

    threading._old_start = threading.Thread.start
    threading.Thread.start = patch_Thread_start(threading._old_start)


def patch_django_mysql_engine(**kw):
    print("=== patch django.db.backends.mysql")

    # print conn connect time for debug
    DEBUG = kw.get("debug", False)
    kw.pop("debug")

    default_pool_kw = {
        'poolclass': pool.QueuePool, 
        'pool_size': 5, 'max_overflow': 0, 'timeout': 10,
        'recycle': 1800, } #'pre_ping': True
    default_pool_kw.update(kw)

    # patch django.db.backends.mysql.base to use sqlalchemy conn pool
    print("=== init sqlalchemy conn pool, size=[%s]" % default_pool_kw['pool_size'])
    base._old_Database = base.Database
    base.Database = pool.manage(base._old_Database, **default_pool_kw)

    def patch_get_new_connection(func):
        pool_conn_keys = {'charset','user','db','database','passwd','password',
            'host','port','client_flag','use_unicode'}
        def new_func(self, conn_params):
            # clean conn_params because sqlalchemy pools key serialization problem
            new_conn_params = {}
            for k in pool_conn_keys:
                if k in conn_params:
                    new_conn_params[k] = conn_params[k]
            # print("### sqlalchemy conn pools status= %s ###" % base.Database.pools)
            if DEBUG:
                t0 = time.time()
            connection = func(self, new_conn_params)
            if DEBUG:
                t1 = time.time()
                print("=== connect mysql host: %s | db: %s | time: %s in thread: %s" % (
                    new_conn_params['host'], new_conn_params['db'] if 'db' in new_conn_params \
                    else new_conn_params['database'], (t1-t0), threading.current_thread().name
                ))
            return connection
        return new_func

    DatabaseWrapper._old_get_new_connection = DatabaseWrapper.get_new_connection
    DatabaseWrapper.get_new_connection = patch_get_new_connection(DatabaseWrapper._old_get_new_connection)

