from .app_properties import AppProperties

# Server socket
#
#   bind - The socket to bind.
#
#       A string of the form: 'HOST', 'HOST:PORT', 'unix:PATH'.
#       An IP is a valid HOST.
#
#   backlog - The number of pending connections. This refers
#       to the number of clients that can be waiting to be
#       served. Exceeding this number results in the client
#       getting an error when attempting to connect. It should
#       only affect servers under significant load.
#
#       Must be a positive integer. Generally set in the 64-2048
#       range.
#
app_props = AppProperties()
# use 'unix:/tmp/gunicorn.sock' when you need to work on nginx, if you do not want to work
#  on NGINX, you need to use the
# 0.0.0.0:5000 instead, read more:
# https://rdmo.readthedocs.io/en/latest/deployment/nginx.html
# https://docs.gunicorn.org/en/stable/deploy.html
# bind = 'unix:/tmp/gunicorn.sock'
bind = '0.0.0.0:5000'
backlog = 2048

#
# Worker processes
#
#   workers - The number of worker processes that this server
#       should keep alive for handling requests.
#
#       A positive integer generally in the 2-4 x $(NUM_CORES)
#       range. You'll want to vary this a bit to find the best
#       for your particular application's work load.
#
#   worker_class - The type of workers to use. The default
#       sync class should handle most 'normal' types of work
#       loads. You'll want to read
#       http://docs.gunicorn.org/en/latest/design.html#choosing-a-worker-type
#       for information on when you might want to choose one
#       of the other worker classes.
#
#       A string referring to a Python path to a subclass of
#       gunicorn.workers.base.Worker. The default provided values
#       can be seen at
#       http://docs.gunicorn.org/en/latest/settings.html#worker-class
#
#   worker_connections - For the eventlet and gevent worker classes
#       this limits the maximum number of simultaneous clients that
#       a single process can handle.
#
#       A positive integer generally set to around 1000.
#
#   timeout - If a worker does not notify the master process in this
#       number of seconds it is killed and a new worker is spawned
#       to replace it.
#
#       Generally set to thirty seconds. Only set this noticeably
#       higher if you're sure of the repercussions for sync workers.
#       For the non sync workers it just means that the worker
#       process is still communicating and is not tied to the length
#       of time required to handle a single request.
#
#   keepalive - The number of seconds to wait for the next request
#       on a Keep-Alive HTTP connection.
#
#       A positive integer. Generally set in the 1-5 seconds range.
#

timeout = app_props.get_timeout()
workers = app_props.get_workers()
preload = True

# Use this instead to use async workers.
# worker_class = 'gevent'
# worker_connections = 1000
# timeout = 120
# keepalive = 2
# threads = 4


#
# Server mechanics
#
#   pidfile - The path to a pid file to write
#
#       A path string or None to not write a pid file.
#

pidfile = '/tmp/gunicorn.pid'

#
#   Logging
#
#   logfile - The path to a log file to write to.
#
#       A path string. "-" means log to stdout.
#
#   loglevel - The granularity of log output
#
#       A string of "debug", "info", "warning", "error", "critical"
#

# errorlog = 'gunicorn_error.log'
errorlog = '-'
loglevel = app_props.get_log_level()
# accesslog = 'gunicorn_access.log'
accesslog = '-'
access_log_format = '%(h)s %({X-Forwarded-For}i)s %(p)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s'
