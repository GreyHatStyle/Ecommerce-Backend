from ._base import BaseAPIView, Request, Response, status, api_exception_handler

class HealthAPI(BaseAPIView):
    """
    Health API to confirm if DRF working or not.
    """
    @api_exception_handler
    def get(self, request: Request):
        
        self.logger.info("Health check")
        
        return Response({
            "status": "success",
            "data": "DRF working fine!!",
        }, status=status.HTTP_200_OK)