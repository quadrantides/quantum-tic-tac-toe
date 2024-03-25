# coding=utf-8
"""
Created on 2022, Jan 1st
@author: patrice journoud
"""
from tornado import gen
from tornado.options import options
import tornado.web

import bokeh
import bokeh.application as bokeh_app
from bokeh.application.handlers import FunctionHandler
from bokeh.embed import server_document

AUTOLOAD_SERVER_URL = options.as_dict()['autoload_server_url']


class StartHandler(tornado.web.RequestHandler):

    @staticmethod
    def modify_doc(doc):
        pass

    _bokeh_app = None

    @classmethod
    def get_bokeh_app(cls):
        if cls._bokeh_app is None:
            cls._bokeh_app = bokeh.application.Application(
                FunctionHandler(
                    StartHandler.modify_doc,
                ),
            )
        return cls._bokeh_app

    @gen.coroutine
    def get(self):
        script = \
            server_document(
                url=AUTOLOAD_SERVER_URL,
            )

        self.render(
            'start.html',
            active_page='inks_upload',
            script=script,
        )
