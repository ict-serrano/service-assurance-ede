from flask import Flask
from flask_restful import Api
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from apispec.ext.marshmallow import MarshmallowPlugin
from ede_service_logger import log, handler, consoleHandler



app = Flask("ede-serrano")
# api = Api(app, version='0.0.1', title='Serrano Event Detection Engine',
#           description="RESTful API for the Serrano Event Detection Engine",
#           )
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Serrano EDE REST API',
        version='v0.1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})


handle_exception = app.handle_exception
handle_user_exception = app.handle_user_exception
app.handle_exception = handle_exception
app.handle_user_exception = handle_user_exception

# Logging
app.logger.addHandler(handler)

api = Api(app)
docs = FlaskApiSpec(app)