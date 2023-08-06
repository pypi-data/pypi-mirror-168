import json
from pathlib import Path
from importlib.resources import read_text

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado

class RouteHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        p = Path('.')
        print(p.absolute())
        self.finish(json.dumps({
            "data": "This is /wooty-woot/get_example endpoint!"
        }))

    @tornado.web.authenticated
    def post(self):
        input_data = self.get_json_body()
        # p = Path('.')
        # (p / input_data['path'] / 'wooty-woot.ipynb').touch()
        nb_content = read_text('wooty_woot.notebooks', 'hello.ipynb')
        response = {
            'filename': 'hello.ipynb',
            'content': nb_content
        }
        self.finish(json.dumps(response))


class RouteHandler2(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        p = Path('.')
        print(p.absolute())
        self.finish(json.dumps({
            "data": "This is /wooty-woot/get_example endpoint!"
        }))

    @tornado.web.authenticated
    def post(self):
        input_data = self.get_json_body()
        p = Path('.')
        nb_content = read_text('wooty_woot.notebooks', 'hello.ipynb')

        (p / input_data['path'] / 'hello.ipynb').write_text(nb_content)
        response = {
            'path': str(Path(input_data['path']) / 'hello.ipynb'),
            'content': ''
        }
        self.finish(json.dumps(response))


def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, "wooty-woot", "viewer")
    route_pattern_2 = url_path_join(base_url, "wooty-woot", "miewer")

    handlers = [
        (route_pattern, RouteHandler),
        (route_pattern_2, RouteHandler2),
    ]

    web_app.add_handlers(host_pattern, handlers)
