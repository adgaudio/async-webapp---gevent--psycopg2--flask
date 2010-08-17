# -*- coding: utf-8 -*-

import jinja2 as jinja

import configuration

_env = {}
loader = jinja.FileSystemLoader(configuration.TEMPLATES)

def template(name):
    template, path, is_uptodate = loader.get_source(_env, name)
    return jinja.Template(template)

def render(template_name, context):
    t = template(template_name)
    return t.render(context)
