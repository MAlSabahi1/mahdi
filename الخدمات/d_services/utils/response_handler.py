from rest_framework import status
from rest_framework.response import Response


class ResponseHandler:
    
    @staticmethod
    def success(message, data=None, extra=None, status_code=status.HTTP_200_OK):

        response = {'message': message, 'success': True}
        if data is not None:
            response['data'] = data
        if extra:
            response.update(extra)
        return Response(response, status=status_code)
    
    @staticmethod
    def error(error, details=None, hint=None, status_code=status.HTTP_400_BAD_REQUEST):

        response = {'error': error, 'success': False}
        if details:
            response['details'] = details
        if hint:
            response['hint'] = hint
        return Response(response, status=status_code)
    
    @staticmethod
    def created(message, data=None, extra=None):
        return ResponseHandler.success(message, data, extra, status.HTTP_201_CREATED)
    
    @staticmethod
    def forbidden(message, hint=None):
        return ResponseHandler.error(message, hint=hint, status_code=status.HTTP_403_FORBIDDEN)
    
    @staticmethod
    def not_found(message, hint=None):
        return ResponseHandler.error(message, hint=hint, status_code=status.HTTP_404_NOT_FOUND)
    
    @staticmethod
    def bad_request(message, details=None, hint=None):
        return ResponseHandler.error(message, details=details, hint=hint, status_code=status.HTTP_400_BAD_REQUEST)
