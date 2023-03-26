from blueprint import app_ns, api_v1

from flask_restx import Resource as ResourceRestx


@api_v1.response(401, 'Unauthorized')
@api_v1.response(403, 'Forbidden')
@api_v1.response(500, 'Internal Server Error')
class Resource(ResourceRestx):
    pass


@app_ns.doc()
class ResourceApp(Resource):
    pass

