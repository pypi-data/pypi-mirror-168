from flask import Blueprint, Flask

bp = Blueprint(
    'user',
    __name__,
    url_prefix='/user',
    template_folder='templates',
    static_folder='static',
)


def init_app(app: Flask) -> None:
    app.register_blueprint(bp)
