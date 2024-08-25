from settings.common.settings import BASE_DIR, INSTALLED_APPS, MIDDLEWARE

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
INSTALLED_APPS += [
    'debug_toolbar',
]

INTERNAL_IPS = [
    '127.0.0.1',
    '192.168.0.170',
    '151.0.50.183',
]

DEBUG = True


def show_toolbar(request):
    return request.user.is_superuser


DEBUG_TOOLBAR_PATCH_SETTINGS = False

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'settings.show_toolbar',
    'INSERT_BEFORE': '</body>',
}

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.cache.CachePanel',
)

import mimetypes
mimetypes.add_type('application/javascript', '.js', True)
