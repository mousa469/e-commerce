from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {
            "status_code": exc.status_code,
            "errors": (
                exc.get_full_details()
                if hasattr(exc, "get_full_details")
                else response.data
            ),
        }

    return response


class CustomNotFound(APIException):
    status_code = 404
    default_code = "Resource_not_found"
    default_detail = "The resource is not found"

    def get_full_details(self):
        return {
            "code": self.default_code,
            "error_message": self.default_detail,
        }


class CustomValidationError(APIException):
    status_code = 400
    default_code = "Not_Valid"
    default_detail = "This operation is not valid"

    def get_full_details(self):
        return {
            "code": self.default_code,
            "error_message": self.detail,
        }
