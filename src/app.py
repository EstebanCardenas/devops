from flask import Flask, jsonify, request
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError
from datetime import datetime
from src.config import Config
import logging
import time
from src.resource.black_lists_resource import (
    BlackListsResource,
    BlackListsEmailResource,
)
from src.resource.auth import AuthResource
from src.resource.test import TestResource
from src.models import Base, engine

app = Flask(__name__)
app.config.from_object(Config)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize JWT
jwt = JWTManager(app)


# JWT Error handlers
@jwt.unauthorized_loader
def unauthorized_callback(callback):
    return jsonify({"message": "Token is required"}), 403


@jwt.invalid_token_loader
def invalid_token_callback(callback):
    return jsonify({"message": "Invalid token"}), 403


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"message": "Token has expired"}), 403


# Handle NoAuthorizationError exception
@app.errorhandler(NoAuthorizationError)
def handle_no_authorization_error(e):
    return jsonify({"message": "Token is required"}), 403


# Request interceptor - logs incoming requests
@app.before_request
def log_request_info():
    request.start_time = time.time()
    logger.info(
        f"Incoming Request: {request.method} {request.path} | "
        f"Remote Address: {request.remote_addr} | "
        f"User Agent: {request.user_agent}"
    )
    if request.method in ["POST", "PUT", "PATCH"]:
        logger.info(
            f"Request Body: {request.get_data(as_text=True)[:500]}"
        )  # Log first 500 chars


# Response interceptor - logs request completion
@app.after_request
def log_response_info(response):
    duration = time.time() - request.start_time if hasattr(request, "start_time") else 0
    logger.info(
        f"Request Complete: {request.method} {request.path} | "
        f"Status: {response.status_code} | "
        f"Duration: {duration:.3f}s"
    )
    return response


@app.route("/health", methods=["GET"])
def health():
    return (
        jsonify(
            {
                "timestamp": datetime.now().isoformat(),
                "message": "OK - this is a new deployment",
            }
        ),
        200,
    )

Base.metadata.create_all(engine)
api = Api(app)

api.add_resource(BlackListsResource, "/blacklists")
api.add_resource(BlackListsEmailResource, "/blacklists/<string:email>")
api.add_resource(AuthResource, "/auth/token")
api.add_resource(TestResource, "/test-res")

if __name__ == "__main__":
    app.run(debug=True)
