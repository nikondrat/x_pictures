import os
import uuid
import logging

from django.utils.deconstruct import deconstructible


def get_logger(name: str):
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    if len(log.handlers) < 1:
        info_format = logging.Formatter("%(asctime)s :: %(levelname)s\n%(message)s\n----------------")
        error_format = info_format
        warning_format = info_format
        debug_format = info_format

        handler_error = logging.StreamHandler()
        handler_error.setLevel(logging.ERROR)
        handler_error.setFormatter(error_format)

        handler_info = logging.StreamHandler()
        handler_info.setLevel(logging.INFO)
        handler_info.setFormatter(info_format)

        handler_warning = logging.StreamHandler()
        handler_warning.setLevel(logging.WARNING)
        handler_warning.setFormatter(warning_format)

        handler_debug = logging.StreamHandler()
        handler_debug.setLevel(logging.DEBUG)
        handler_debug.setFormatter(debug_format)

        log.addHandler(handler_error)
        log.addHandler(handler_info)
    return log


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(str(uuid.uuid4()), ext)
        return os.path.join(self.path, filename)
