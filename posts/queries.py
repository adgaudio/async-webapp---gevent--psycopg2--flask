# -*- coding: utf-8 -*-


from utils import query



class TopPosts(query.SQLQuery):
    name = 'top_posts'
    sql = '''
            SELECT p.*, ARRAY(SELECT t.name || ' ' || t.path FROM tags t, tags_posts tp WHERE tp.posts_id = p.id AND tp.tags_path = t.path) AS tags 
            FROM posts p 
            WHERE p.public = %s
            ORDER BY p.created LIMIT %s;
        '''

    def __init__(self, limit=10, public=True):
        self.params = (public, limit)



class TopPostsByTag(TopPosts):
    name = 'top_posts'
    sql =  '''
            SELECT p.*, ARRAY(SELECT t.name || ' ' || t.path FROM tags t, tags_posts tp WHERE tp.posts_id = p.id AND tp.tags_path = t.path) AS tags 
            FROM posts p, tags_post tp
            WHERE 
                tp.path = %s
                AND tp.post_id = p.id
                AND p.public = %s
            ORDER BY p.created LIMIT %s;
        '''

    def __init__(self, filter_by_tag, limit=10, public=True):
        self.params = (filter_by_tag, public, limit)
