from src.views.blueprint import api, app_ns
from flask_restx import Resource as ResourceRestx


@api.response(401, 'Unauthorized')
@api.response(403, 'Forbidden')
@api.response(500, 'Internal Server Error')
class Resource(ResourceRestx):
    pass


@app_ns.doc()
class ResourceApp(Resource):
    pass
