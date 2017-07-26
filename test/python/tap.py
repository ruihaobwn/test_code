from webob import Request,Response
import webob.dec
import webob.exc
import simplejson
import routes.middleware
import uuid

class Controller:
    def __init__(self):
        self.instances={}

    @webob.dec.wsgify
    def __call__(self, req):
        arg_dict = req.environ['wsgiorg.routing_args'][1]
        action = arg_dict.pop('action')
        del arg_dict['controller']
        method = getattr(self,action)
        result= method(req,**arg_dict)

        if result is None:
            return webob.Response(body='',
                                  status='204 Not Found',
                                  headerlist=[('Content-Type','application/json')])
        else:
            if not isinstance(result,basestring):
                result = simplejson.dumps(result)
                return result

    def create(self,req):
        print(req.params)
        name=req.params['name']
        if name:
            inst_id=str(uuid.uuid4())
            inst={'id':inst_id,
                  'name':name}
            self.instances[inst_id]=inst
            return {'instance':inst}

    def show(self,req,instance_id):
        inst=self.instances.get(instance_id)
        print inst
        return {'instance':inst}


class Routes(object):
    def __init__(self):
        self._mapper=routes.Mapper()
        self.add_routes()
        self._router=routes.middleware.RoutesMiddleware(self._dispatch,
                                                        self._mapper)

    def add_routes(self):
        controller = Controller()
        self._mapper.connect("/instances",
                             controller=controller,action="create",
                             conditions=dict(method=["POST"])
                             )

        self._mapper.connect("/instances",
                             controller=controller,action="index",
                             conditions=dict(method=["GET"]))

        self._mapper.connect("/instances/{instance_id}",
                             controller=controller,action="show",
                             conditions=dict(method=["GET"]))

        self._mapper.connect("/instances/{instance_id}",
                             controller=controller,action="update",
                             conditions=dict(method=["PUT"]))

        self._mapper.connect("/instances/{instance_id}",
                             controller=controller,action="delete",
                             conditions=dict(method=["DELETE"]))


    @webob.dec.wsgify
    def __call__(self, req):
        return self._router

    @staticmethod
    @webob.dec.wsgify
    def _dispatch(req):
        match=req.environ['wsgiorg.routing_args'][1]
        if not match:
            return webob.exc.HTTPNotFound()

        app = match['controller']
        return app

# @wsgify
# def test(req):
#     res = Response()
#     res.status = 200
#     res.body   = "spch"
#     return res
app = Routes()
# class Tab(object):
#     def __call__(self, environ, start_response):
#         req = Request(environ)
#         return test(environ,start_response)

def app_factory(glocal_config,**local_config):
    return app