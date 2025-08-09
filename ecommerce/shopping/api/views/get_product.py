from ._base import BaseAPIView, Response, Request, status, api_exception_handler
from ..throttles import BurstRateThrottle, SustainedRateThrottle
from shopping.models import Product
from .._serializers import ProductSerializer
from django.core.exceptions import ObjectDoesNotExist

class GetProductAPI(BaseAPIView):
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]
    
    @api_exception_handler
    def get(self, request: Request, prod_id:str | None):
        
        if prod_id is None:
            return Response({
                "status":"failed",
                "message": "Kindly provide product uuid in URL",
            }, status=status.HTTP_400_BAD_REQUEST)
        
        
        try:
            product = Product.objects.get(id=prod_id)
            
        except ObjectDoesNotExist:
            return Response({
                "status":"failed",
                "message": "Wrong product id given",
            }, status=status.HTTP_400_BAD_REQUEST)
        
        product_serializer = ProductSerializer(product)
        
        return Response({
            "status":"success",
            "product": product_serializer.data,
        }, status=status.HTTP_200_OK)
        
        