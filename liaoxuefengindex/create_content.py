__author__ = 'yukai'

def create_content(real_content):
    with open('./template.html', 'r') as f:
        content = f.read()
        content = content.replace("{content}", real_content)
        return content


def _create_memcache_client():
    try:
        import pylibmc
        return pylibmc.Client()
    except ImportError:
        import memcache
        return memcache.Client(['127.0.0.1:11211'])
cache = _create_memcache_client()