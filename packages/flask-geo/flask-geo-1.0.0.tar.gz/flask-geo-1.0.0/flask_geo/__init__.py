from flask import Flask


class FlaskGeo:

    def __init__(self, app: Flask = None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        pass
