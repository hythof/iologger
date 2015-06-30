## What IS It?
Keep a IO log for Django.

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
