import web
__author__ = 'yukai'

urls = (
    '/', 'index'
)
app = web.application(urls, globals())
