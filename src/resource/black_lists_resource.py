import uuid
from flask_restful import Resource
from flask import request
from src.logic.email import run_block_email_validations
from src.models import session, BlockedEmail
from flask_jwt_extended import jwt_required, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError, JWTDecodeError
from jwt.exceptions import DecodeError
from werkzeug.exceptions import BadRequest


class BlackListsResource(Resource):
    def __validate_token(self):
        try:
            verify_jwt_in_request()
        except NoAuthorizationError:
            return {"message": "Token is required"}, 403
        except (JWTDecodeError, DecodeError):
            return {"message": "Invalid token"}, 403

    def post(self):
        validate_token_result = self.__validate_token()
        if validate_token_result:
            return validate_token_result

        data = request.get_json()
        email = data.get("email")
        app_uuid = data.get("app_uuid")
        blocked_reason = data.get("blocked_reason")

        validations_result = run_block_email_validations(
            email, app_uuid, blocked_reason
        )
        if validations_result:
            raise BadRequest(validations_result["message"])

        try:
            blocked_email = BlockedEmail(
                email=email,
                app_uuid=uuid.UUID(app_uuid),
                blocked_reason=blocked_reason,
                request_ip=request.remote_addr or "unknown",
            )
            session.add(blocked_email)
            session.commit()

            return {"message": "Email blocked successfully"}, 201
        except Exception as e:
            session.rollback()
            return {"message": f"Database error: {str(e)}"}, 500

    def delete(self):
        validate_token_result = self.__validate_token()
        if validate_token_result:
            return validate_token_result

        session.query(BlockedEmail).delete()
        session.commit()
        return {"message": "All blocked emails deleted successfully"}, 200


class BlackListsEmailResource(Resource):
    def __validate_token(self):
        try:
            verify_jwt_in_request()
        except NoAuthorizationError:
            return {"message": "Token is required"}, 403
        except (JWTDecodeError, DecodeError):
            return {"message": "Invalid token"}, 403

    def get(self, email: str):
        validate_token_result = self.__validate_token()
        if validate_token_result:
            return validate_token_result

        db_email = session.query(BlockedEmail).filter_by(email=email).first()

        result = {"blocked": False}
        if db_email:
            result = {"blocked": True}
            if db_email.blocked_reason:
                result["blocked_reason"] = db_email.blocked_reason

        return result, 200
