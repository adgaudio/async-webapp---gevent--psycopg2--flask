# -*- coding: utf-8 -*-

import re
from app import app

_rx = re.compile(r'[^\w]+')

@app.template_filter('slugify')
def slugify(text, delim='-'):
    return unicode(_rx.sub(text, delim))
