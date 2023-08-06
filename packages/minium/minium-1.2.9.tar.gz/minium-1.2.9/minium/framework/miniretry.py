#!/usr/bin/env python3
from .log_color import *

logger = logging.getLogger("minium")


def retry(times):
    def wrapper(func):
        def exe(*args, **kwargs):
            n = 1
            while n < times:
                try:
                    logger.info("第 %d 次运行 %s" % (n, func.__name__))
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.exception(e)
                    n += 1
            else:
                logger.info("最后一次")
                return func(*args, **kwargs)

        return exe

    return wrapper
