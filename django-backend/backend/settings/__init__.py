from __future__ import absolute_import

from .common import *

if os.getenv('NETWORK', 'PROD') == 'STAGE':
    from .stage import *
elif os.getenv('NETWORK', 'PROD') == 'TEST':
    from .test import *
elif os.getenv('NETWORK', 'PROD') == 'DEV':
    from .dev import *


if not DEBUG:
    import sentry_sdk
    sentry_sdk.init(
        dsn='https://3dbcf56e158d4dafb07954f160972c19@sentry.x-pictures.io/2',
        traces_sample_rate=1.0,
    )
