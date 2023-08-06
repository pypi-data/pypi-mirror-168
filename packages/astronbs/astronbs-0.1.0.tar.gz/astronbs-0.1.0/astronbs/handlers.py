import json
from pathlib import Path
from importlib.resources import files

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado


def hello():
    """
    Return the contents of the hello world notebook.
    """
    return files('astronbs').joinpath('notebooks').joinpath('reduction-template.ipynb').read_text()


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
        p = Path('.')
        nb_content = hello()

        (p / input_data['path'] / 'reduction_template.ipynb').write_text(nb_content)
        response = {
            'path': str(Path(input_data['path']) / 'reduction_template.ipynb'),
            'content': ''
        }
        self.finish(json.dumps(response))


def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, "astronbs", "reduction_template")
    handlers = [(route_pattern, RouteHandler)]
    web_app.add_handlers(host_pattern, handlers)
