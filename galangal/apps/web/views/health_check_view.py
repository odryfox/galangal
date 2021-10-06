from flask import Response
from flask.views import MethodView


class HealthCheckView(MethodView):

    def get(self):
        return Response(status=200)
