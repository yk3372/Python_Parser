__author__ = 'yukai'

def _create_db():
    # 本地环境
    host = 'localhost'
    db = 'weather'
    port = 3306
    user = 'weather'
    pw = 'weather'
    try:
        import sae.const
        db = sae.const.MYSQL_DB
        user = sae.const.MYSQL_USER
        pw = sae.const.MYSQL_PASS
        host = sae.const.MYSQL_HOST
        port = int(sae.const.MYSQL_PORT)
    except ImportError:
        pass
    # return web.database(dbn='mysql', host=host, port=port, db=db, user=user, pw=pw)
# db = _create_db()