from starlette.applications import Starlette, BaseHTTPMiddleware
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware

from .global_state import GlobalStateMiddleware
from .minification import install_html_minification_hooks
from .precomputation import Precomputation
from .templating import register_template_global


class Comet(Starlette):
    def __init__(self):
        super().__init__(middleware=[Middleware(GlobalStateMiddleware)])

    def setup_precomputation(self, precomp_package):
        self.precomputation = Precomputation(precomp_package)
        register_template_global("precomp", self.precomputation)

    def setup_html_minification(self, **config):
        install_html_minification_hooks(**config)

    def add_static_folder(
        self, directory: str, path: str = None, name: str = None, **kwargs
    ):
        if path is None:
            path = "/" + directory

        self.mount(path, StaticFiles(directory=directory, **kwargs), name)