# -*- coding: utf-8 -*-

from . import controllers
from . import models
import logging


_logger = logging.getLogger(__name__)



def pre_init_hook(cr):
    _logger.info(' pre_init_hook')

def post_init_hook(cr,registry):
    _logger.info(' post_init_hook')


def uninstall_hook(cr,registry):
    _logger.info(' post_init_hook')