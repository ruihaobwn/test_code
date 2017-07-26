if __name__ == '__main__':
    from eventlet import wsgi
    import eventlet
    from paste import httpserver
    from paste.deploy import loadapp
    app = loadapp('config:configured.ini',relative_to='.');
    wsgi.server(eventlet.listen(('',8080)),app)
    # httpserver.serve(loadapp('config:configured.ini',relative_to='.'),
    #         host='0.0.0.0',port='8080')
