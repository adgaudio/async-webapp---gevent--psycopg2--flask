import os

PROJ_DIR = os.path.dirname(__file__)
TEMPLATES = (
    os.path.join(PROJ_DIR, 'templates')
)
DATABASES = {
}
APPLICATIONS = (
    'posts',
    'tags',
)
DEBUG = True

try:
    from settings_locals import *
except ImportError:
    pass
