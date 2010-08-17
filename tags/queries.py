# -*- coding: utf-8 -*-


from utils import query


class TopTags(query.SQLQuery):
    name = 'top_tags'
    sql = '''
        SELECT t.name, sum(1) AS sum
        FROM tags t, tags_posts tp 
        WHERE t.path = tp.tags_path GROUP BY t.name
        LIMIT %s
        '''

    def __init__(self, limit=20):
        self.params = (limit, )
