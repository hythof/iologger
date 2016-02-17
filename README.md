## What is it?
Show IO log for Django.
It information helpful for development.

Support IO
- redis
- MySQL-python

## Quick start for Django

Add your settings.py

    # add settings.py
    add_middleware = ('iologger.middleware.IOLoggerMiddleware',)
    MIDDLEWARE_CLASSES = add_middleware + MIDDLEWARE_CLASSES

Example output

    # ./manage.py runserver_plus
    -- GET /ex_admin/ 302
    -- GET /admin/login/ 200
    [mysql] SET SQL_AUTO_IS_NULL = 0
    [mysql] SELECT * FROM `django_site` WHERE `django_site`.`id` = 1 LIMIT 21
    -- POST /admin/login/ 302
    [mysql] SET SQL_AUTO_IS_NULL = 0
    [mysql] SELECT * FROM `auth_user` WHERE `auth_user`.`username` = 'admin' LIMIT 21
    [mysql] UPDATE `auth_user` SET `last_login` = '2015-05-20 09:35:23' WHERE `auth_user`.`id` = 1
    -- GET /ex_admin/ 200
    [mysql] SET SQL_AUTO_IS_NULL = 0
    [mysql] SELECT * FROM `auth_user` WHERE `auth_user`.`id` = 1 LIMIT 21

## Settings

Add your settings.py

    IOLogger = {
        'filter': ['redis', 'mysql'],  # targets
        'output': sys.stdout.write,    # output log function
    }

## More detail information

Show stack trace at IO and filter regex example.

    # env show_stack="MySQLdb/cursors.py:164|cursor.execute" ./manage.py runserver_plus
    -- GET /admin/login/ 200
    [mysql] SET SQL_AUTO_IS_NULL = 0
        /home/bar/.virtualenvs/foo/local/lib/python2.7/site-packages/django/contrib/auth/views.py:50      | current_site = get_current_site(request)
        /home/bar/.virtualenvs/foo/local/lib/python2.7/site-packages/django/db/models/sql/compiler.py:784 | cursor = self.connection.cursor()
        /home/bar/.virtualenvs/foo/local/lib/python2.7/site-packages/django/db/backends/__init__.py:133   | self.connect()
    [mysql] SELECT * FROM `django_site` WHERE `django_site`.`id` = 1 LIMIT 21
        /home/bar/.virtualenvs/foo/local/lib/python2.7/site-packages/django/contrib/auth/views.py:50 | current_site = get_current_site(request)


Show full stack trace.

    # env show_stack=. ./manage.py runserver_plus
    -- GET /admin/login/ 200
    [mysql] SET SQL_AUTO_IS_NULL = 0
        /usr/lib/python2.7/threading.py:783                                                                    | self.__bootstrap_inner()
        /usr/lib/python2.7/threading.py:810                                                                    | self.run()
        /usr/lib/python2.7/threading.py:763                                                                    | self.__target(*self.__args, **self.__kwargs)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/werkzeug/serving.py:602                   | passthrough_errors, ssl_context).serve_forever()
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/werkzeug/serving.py:462                   | HTTPServer.serve_forever(self)
        /usr/lib/python2.7/SocketServer.py:238                                                                 | self._handle_request_noblock()
        /usr/lib/python2.7/SocketServer.py:295                                                                 | self.process_request(request, client_address)
        /usr/lib/python2.7/SocketServer.py:321                                                                 | self.finish_request(request, client_address)
        /usr/lib/python2.7/SocketServer.py:334                                                                 | self.RequestHandlerClass(request, client_address, self)
        /usr/lib/python2.7/SocketServer.py:655                                                                 | self.handle()
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/werkzeug/serving.py:203                   | rv = BaseHTTPRequestHandler.handle(self)
        /usr/lib/python2.7/BaseHTTPServer.py:340                                                               | self.handle_one_request()
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/werkzeug/serving.py:238                   | return self.run_wsgi()
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/werkzeug/serving.py:180                   | execute(self.server.app)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/werkzeug/serving.py:170                   | for data in application_iter:
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/werkzeug/debug/__init__.py:89             | for item in app_iter:
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/werkzeug/debug/__init__.py:88             | app_iter = self.app(environ, start_response)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/contrib/staticfiles/handlers.py:64 | return self.application(environ, start_response)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/core/handlers/wsgi.py:187          | response = self.get_response(request)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/core/handlers/base.py:111          | response = wrapped_callback(request, *callback_args, **callback_kwargs)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/views/decorators/cache.py:52       | response = view_func(request, *args, **kwargs)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/contrib/admin/sites.py:361         | return login(request, **defaults)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/views/decorators/debug.py:76       | return view(request, *args, **kwargs)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/utils/decorators.py:105            | response = view_func(request, *args, **kwargs)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/views/decorators/cache.py:52       | response = view_func(request, *args, **kwargs)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/contrib/auth/views.py:50           | current_site = get_current_site(request)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/contrib/sites/shortcuts.py:15      | return Site.objects.get_current()
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/contrib/sites/models.py:54         | current_site = self.get(pk=sid)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/models/manager.py:92            | return getattr(self.get_queryset(), name)(*args, **kwargs)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/models/query.py:351             | num = len(clone)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/models/query.py:122             | self._fetch_all()
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/models/query.py:966             | self._result_cache = list(self.iterator())
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/models/query.py:265             | for row in compiler.results_iter():
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/models/sql/compiler.py:700      | for rows in self.execute_sql(MULTI):
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/models/sql/compiler.py:784      | cursor = self.connection.cursor()
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/backends/__init__.py:165        | cursor = self.make_debug_cursor(self._cursor())
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/backends/__init__.py:138        | self.ensure_connection()
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/backends/__init__.py:133        | self.connect()
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/backends/__init__.py:124        | self.init_connection_state()
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/backends/mysql/base.py:483      | cursor.execute('SET SQL_AUTO_IS_NULL = 0')
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/backends/utils.py:81            | return super(CursorDebugWrapper, self).execute(sql, params)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/backends/utils.py:63            | return self.cursor.execute(sql)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/backends/mysql/base.py:129      | return self.cursor.execute(query, args)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/MySQLdb/cursors.py:164                    | def execute(self, query, args=None):
    [mysql] SELECT * FROM `django_site` WHERE `django_site`.`id` = 1 LIMIT 21
        /usr/lib/python2.7/threading.py:783                                                                    | self.__bootstrap_inner()
        /usr/lib/python2.7/threading.py:810                                                                    | self.run()
        /usr/lib/python2.7/threading.py:763                                                                    | self.__target(*self.__args, **self.__kwargs)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/werkzeug/serving.py:602                   | passthrough_errors, ssl_context).serve_forever()
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/werkzeug/serving.py:462                   | HTTPServer.serve_forever(self)
        /usr/lib/python2.7/SocketServer.py:238                                                                 | self._handle_request_noblock()
        /usr/lib/python2.7/SocketServer.py:295                                                                 | self.process_request(request, client_address)
        /usr/lib/python2.7/SocketServer.py:321                                                                 | self.finish_request(request, client_address)
        /usr/lib/python2.7/SocketServer.py:334                                                                 | self.RequestHandlerClass(request, client_address, self)
        /usr/lib/python2.7/SocketServer.py:655                                                                 | self.handle()
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/werkzeug/serving.py:203                   | rv = BaseHTTPRequestHandler.handle(self)
        /usr/lib/python2.7/BaseHTTPServer.py:340                                                               | self.handle_one_request()
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/werkzeug/serving.py:238                   | return self.run_wsgi()
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/werkzeug/serving.py:180                   | execute(self.server.app)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/werkzeug/serving.py:170                   | for data in application_iter:
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/werkzeug/debug/__init__.py:89             | for item in app_iter:
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/werkzeug/debug/__init__.py:88             | app_iter = self.app(environ, start_response)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/contrib/staticfiles/handlers.py:64 | return self.application(environ, start_response)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/core/handlers/wsgi.py:187          | response = self.get_response(request)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/core/handlers/base.py:111          | response = wrapped_callback(request, *callback_args, **callback_kwargs)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/views/decorators/cache.py:52       | response = view_func(request, *args, **kwargs)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/contrib/admin/sites.py:361         | return login(request, **defaults)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/views/decorators/debug.py:76       | return view(request, *args, **kwargs)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/utils/decorators.py:105            | response = view_func(request, *args, **kwargs)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/views/decorators/cache.py:52       | response = view_func(request, *args, **kwargs)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/contrib/auth/views.py:50           | current_site = get_current_site(request)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/contrib/sites/shortcuts.py:15      | return Site.objects.get_current()
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/contrib/sites/models.py:54         | current_site = self.get(pk=sid)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/models/manager.py:92            | return getattr(self.get_queryset(), name)(*args, **kwargs)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/models/query.py:351             | num = len(clone)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/models/query.py:122             | self._fetch_all()
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/models/query.py:966             | self._result_cache = list(self.iterator())
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/models/query.py:265             | for row in compiler.results_iter():
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/models/sql/compiler.py:700      | for rows in self.execute_sql(MULTI):
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/models/sql/compiler.py:786      | cursor.execute(sql, params)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/backends/utils.py:81            | return super(CursorDebugWrapper, self).execute(sql, params)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/backends/utils.py:65            | return self.cursor.execute(sql, params)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/django/db/backends/mysql/base.py:129      | return self.cursor.execute(query, args)
        /home/foo/.virtualenvs/bar/local/lib/python2.7/site-packages/MySQLdb/cursors.py:164                    | def execute(self, query, args=None):
