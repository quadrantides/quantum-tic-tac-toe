# -*- coding: utf-8 -*-
"""
Created on 2022, Jan 1st
@author: patrice journoud
"""
import os
import logging

# Constants for application localization

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    level=logging.INFO
)
LOGGER = logging.getLogger("app_qt3")
