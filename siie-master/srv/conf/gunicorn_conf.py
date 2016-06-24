bind = "unix:/home/karatbars/webapps/karatbars/srv/run/gunicorn.sock"
workers = 2
name = "karatbars"
loglevel = "error"
max_requests = 1000
errorlog = "/home/karatbars/webapps/karatbars/srv/logs/gunicorn.err.log"