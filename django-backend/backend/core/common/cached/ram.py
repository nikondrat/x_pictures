import inspect
import operator
from hashlib import sha1
from functools import reduce
from functools import wraps, partial
from datetime import timedelta, datetime

from django.core.cache import cache
from django.conf import settings
from django.utils.encoding import smart_str
from django.utils import translation
from django.db import models


class Cached:
    def __init__(
            self, slot_name=None, timeout=None,
            use_inner_cache=False, only_inner_cache=False,
            vary_on=None, vary_on_language=False
    ):
        self._slot_name = slot_name
        self._timeout = timeout
        self._use_inner_cache = use_inner_cache
        self._only_inner_cache = only_inner_cache
        self._vary_on = vary_on
        self._cache = {}
        self._vary_on_language = vary_on_language

    def __call__(self, func):
        def wrapped(*args, **kwargs):
            key = self.get_slot_name(func, args, kwargs)
            result = None

            if self._use_inner_cache or self._only_inner_cache:
                r, t = self._cache.get(key, (None, datetime.min))
                if datetime.now() <= t + timedelta(seconds=self._timeout):
                    result = r
                else:
                    self._cache.pop(key, None)

                if result is None and not self._only_inner_cache:
                    result = cache.get(key)
                    if result:
                        self._cache[key] = (result, datetime.now())
            else:
                result = cache.get(key)

            if result is None:
                result = func(*args, **kwargs)

                if self._use_inner_cache or self._only_inner_cache:
                    self._cache[key] = (result, datetime.now())

                if not self._only_inner_cache:
                    cache.set(key, result, self._timeout)

            return result

        wrapped.invalidate = partial(self.invalidate, func)
        wrapped.uncached = func
        return wraps(func)(wrapped)

    @classmethod
    def _default_vary_on(cls, func, *args, **kwargs):
        args_names = inspect.getfullargspec(func)[0]
        if len(args_names) > 0 and args_names[0] in ('self', 'cls'):
            args = args[1:]
            args_names = args_names[1:]
        params = kwargs.copy()
        for q, arg_value in enumerate(args):
            try:
                arg_name = args_names[q]
            except IndexError:
                arg_name = 'arg_{}'.format(q)
            if arg_name not in params:
                params[arg_name] = arg_value
        result = []
        for k, v in sorted(params.items(), key=lambda x: x[0]):
            result.extend([k, v.pk if isinstance(v, models.Model) else v])
        return result

    def get_slot_name(self, func, args, kwargs):
        params = self._vary_on(*args, **kwargs) if self._vary_on else self._default_vary_on(func, *args, **kwargs)
        if self._vary_on_language:
            params = list(params)
            params.append(translation.get_language())
        return u':'.join([
            getattr(settings, 'CACHE_KEY_PREFIX', getattr(settings, 'KEY_PREFIX', u'')),
            self._slot_name or u'{}.{}'.format(
                str(func.__module__),
                str(func.__name__)
            ),
            sha1(reduce(operator.add, map(smart_str, params)).encode('utf8')).hexdigest() if params else u'',
        ])

    def invalidate(self, func, *args, **kwargs):
        key = self.get_slot_name(func, args, kwargs)
        cache.delete(key)
        self._cache = {}
