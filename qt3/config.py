# coding=utf-8
"""
Created on 2022, Jan 1st
@author: patrice journoud
"""
from datetime import datetime as dt
from tornado.options import define

ENVIRONMENT = "dev"
VERSION = "1.0"
DATES = dt.now().strftime("%Y")

default_port = 8052

define("port", default=default_port, help="runs app qt3 on the given port", type=int)

define(
    "app url basename",
    default="qt3",
    help="URL to indicate the QT3 Development Version",
    type=str
)

default_server_port = 5000

define("server_port", default=default_server_port, help="runs app qt3 on the given server port", type=int)

SERVER_PORT = default_server_port
SERVER_URL = "qt3/{}".format(ENVIRONMENT)
define("server url", default=SERVER_URL, help="Bokeh Server URL", type=str)

AUTOLOAD_SERVER_URL = 'http://localhost:{}/{}'.format(SERVER_PORT, SERVER_URL)

define("autoload_server_url", default=AUTOLOAD_SERVER_URL, help="runs server on the given port", type=str)
