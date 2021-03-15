import logging
from datetime import date
from time import perf_counter

from django.utils.timezone import localtime

logger = logging.getLogger(__name__)


class Utility:

    @staticmethod
    def get_local_datetime_as_str(date_obj: date) -> str:
        return localtime(date_obj).strftime('%Y-%m-%d %H:%M')

    @staticmethod
    def time_it(foo_name: str):
        def decor_0(foo):
            def decor_1(*args, **kwargs):
                time_0 = perf_counter()
                result = foo(*args, **kwargs)
                logger.debug('time_it(): %s = %.4f' % (foo_name, perf_counter() - time_0))
                return result

            return decor_1

        return decor_0
