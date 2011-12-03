# -*- coding: utf-8 -*-

import time

from flask import render_template
from app import app

from utils import db, query
from posts import queries as posts_queries
from tags import queries as tags_queries


@app.route('/')
def index(limit=10):
    ctx = {}
    results = db.fetch(
        posts_queries.TopPosts(limit),
        tags_queries.TopTags(20)
    )
    ctx.update(results)
    return render_template('post_list.html', **ctx)

@app.route('/tags/<path:tag>')
def filter_by_tag(tag, limit=10):
    ctx = {}
    results = db.fetch(
        posts_queries.TopPostsByTag(tag, limit),
        tags_queries.TopTags(20)
    )
    ctx.update(results)
    return render_template('post_list.html', **ctx)

@app.route('/sleeptest/<int:sleep>/')
@app.route('/sleeptest/<int:sleep>/<int:queries_number>/')
def sleep_test(sleep, queries_number=10):
    start_time = time.time()
    queries = []
    for i in xrange(queries_number):
        q_name = 'sleeptest_%d' % i
        queries.append(query.SQLQuery(q_name, 'SELECT pg_sleep(%s)', (sleep, )))
    results = db.fetch(*queries)
    work_time = time.time() - start_time
    return """
    <!doctype html>
    <html>
    <body>
        <div style="text-align:center">
            <h3>%d queries making %d second sleep</h3>
            <h2>total work time: %.2fsec</h2>
        </div>
    </body>
    </html>
    """ % (queries_number, sleep, work_time)
