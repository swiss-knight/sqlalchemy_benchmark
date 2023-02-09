# Benchmark of SQLAlchemy 2.0.x engine

1. Spin up the database:
```sh
docker compose up --build -d db && docker compose logs --tail 100 -f db
```

2. Once the database system is ready to accept connections, quit the log with Ctrl+C and spin up multiple instances of the app:
```sh
docker compose up --build -d --scale app=5 app && docker compose logs --tail 100 -f app
```

3. With the PostgreSQL admin tool of your choice, e.g. pgAdmin4, run this SQL snippet to monitor the ghost database slots which stay open:

```sql
SELECT state, query, *
  FROM pg_stat_activity
 WHERE application_name NOT ILIKE '%pgAdmin 4%';

```

4.

If you spin up 10 instances of the app instead of 5:
```sh
docker compose up --build -d --scale app=10 app && docker compose logs --tail 100 -f app
```

you will certainly face the SQLALchemy error:

```python
Traceback (most recent call last):
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3269, in raw_connection
    return self.pool.connect()
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 1255, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 716, in checkout
    rec = pool._do_get()
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/impl.py", line 168, in _do_get
    with util.safe_reraise():
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 147, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/impl.py", line 166, in _do_get
    return self._create_connection()
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 393, in _create_connection
    return _ConnectionRecord(self)
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 678, in __init__
    self.__connect()
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 902, in __connect
    with util.safe_reraise():
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 147, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 898, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/engine/create.py", line 640, in connect
    return dialect.connect(*cargs, **cparams)
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/engine/default.py", line 580, in connect
    return self.loaded_dbapi.connect(*cargs, **cparams)
  File "/usr/local/lib/python3.10/site-packages/psycopg2/__init__.py", line 122, in connect
    conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
psycopg2.OperationalError: FATAL:  sorry, too many clients already


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/test.py", line 42, in <module>
    foo()
  File "/app/test.py", line 19, in foo
    with engine.begin() as connection:
  File "/usr/local/lib/python3.10/contextlib.py", line 135, in __enter__
    return next(self.gen)
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3209, in begin
    with self.connect() as conn:
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3245, in connect
    return self._connection_cls(self)
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 147, in __init__
    Connection._handle_dbapi_exception_noconnection(
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 2410, in _handle_dbapi_exception_noconnection
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
    self._dbapi_connection = engine.raw_connection()
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3269, in raw_connection
    return self.pool.connect()
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 452, in connect
    return _ConnectionFairy._checkout(self)
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 1255, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 716, in checkout
    rec = pool._do_get()
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/impl.py", line 168, in _do_get
    with util.safe_reraise():
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 147, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/impl.py", line 166, in _do_get
    return self._create_connection()
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 393, in _create_connection
    return _ConnectionRecord(self)
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 678, in __init__
    self.__connect()
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 902, in __connect
    with util.safe_reraise():
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 147, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 898, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/engine/create.py", line 640, in connect
    return dialect.connect(*cargs, **cparams)
  File "/usr/local/lib/python3.10/site-packages/sqlalchemy/engine/default.py", line 580, in connect
    return self.loaded_dbapi.connect(*cargs, **cparams)
  File "/usr/local/lib/python3.10/site-packages/psycopg2/__init__.py", line 122, in connect
    conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) FATAL:  sorry, too many clients already

(Background on this error at: https://sqlalche.me/e/20/e3q8)

```


