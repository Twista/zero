from typing import Optional, Type

from flask import Flask, request, jsonify

from src.config import config_map, Config
from src.modules.task_module import bp


def create_app(config_name: Optional[str] = None):
    config: Type[Config] = config_map[config_name]
    app = Flask(__name__)

    init_error_handlers(app)
    setup_app(app)

    app.url_map.strict_slashes = False  # fixme: remove
    app.config.from_object(config)
    return app


def init_error_handlers(app):
    # define error callbacks
    def _get_request_data():
        return None

    def internal_server_error(error):
        print((error, dir(error)))
        app.logger.exception(
            f"Error-500, url: {request.url} args: {request.args.to_dict()} body: {_get_request_data()}")
        return jsonify({
            "error": 500,
            "error_message": error.description
        }), 500

    def not_found(error):
        app.logger.warn(f"Error-404, url: {request.url} args: {request.args.to_dict()} body: {_get_request_data()}")
        return jsonify({
            "error": 404,
            "error_message": error.description
        }), 404

    def unauthorized_exception(error):
        app.logger.exception(
            f"Error-403, url: {request.url} args: {request.args.to_dict()} body: {_get_request_data()}")
        return jsonify({
            "error": 403,
            "error_message": error.description
        }), 403

    def bad_request(error):
        app.logger.exception(
            f"Error-400, url: {request.url} args: {request.args.to_dict()} body: {_get_request_data()}")
        return jsonify({
            "error": 400,
            "error_message": error.description
        }), 400

    # register error callbacks with proper code or exception
    app.register_error_handler(Exception, internal_server_error)
    app.register_error_handler(500, internal_server_error)

    app.register_error_handler(404, not_found)

    app.register_error_handler(403, unauthorized_exception)

    app.register_error_handler(400, bad_request)
    app.register_error_handler(405, bad_request)


def setup_app(app):
    init_error_handlers(app)

    """
    @app.before_request
    def before_request():
        with sentry_sdk.configure_scope() as scope:
            scope.set_tag('api-g-request-Id',
                          request.environ.get('serverless.event', {}).get('requestContext', {}).get('requestId', None))
        log.info(request.environ.get('serverless.event'))
        log.debug(request.url)
    """

    @app.before_request
    def before_request_func():
        print("before_request executing!")
        print(request.url)

    @app.after_request
    def add_header(response):
        # disable location autocorrect to avoid HTTP redirects in HTTPS context
        response.autocorrect_location_header = False
        return response

    @app.route("/", methods=["GET"])
    def hello():
        return jsonify({
            "Hello": "World"
        })

    app.register_blueprint(bp)
