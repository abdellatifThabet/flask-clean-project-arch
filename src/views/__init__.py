from flask import Response
from typing import Dict
import json

def json_response(data: Dict=None, trace=None, status_code: int = 200,
                   mimetype="application/json") -> Response:

   return Response(
        response=json.dumps({
            "data": data,
            "trace": trace
        }),
        status=status_code,
        mimetype=mimetype
    )