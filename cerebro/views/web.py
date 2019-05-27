from sanic import response
from sanic.views import HTTPMethodView


class HtmlView(HTTPMethodView):
    @staticmethod
    async def get(request):
        return response.html('<p>Hello world!</p>')
