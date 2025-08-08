from typing import Any, Dict, cast

from shopping.models import Product
from shopping.utils import ProductRecommendationUtil

from .._serializers import ProductSerializer, ValidateSearchQuery
from ..throttles import BurstRateThrottle, SustainedRateThrottle
from ._base import (BaseAPIView, Request, Response, api_exception_handler,
                    status)


class SearchProductsAPI(BaseAPIView):
    """
    Returns `n` number of products using recommendation system
    """
    recommendation = ProductRecommendationUtil()
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]
    
    @api_exception_handler
    def post(self, request: Request, count: int) -> Response:
        
        serializer = ValidateSearchQuery(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "failed",
                "errors": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # I have checked for None type above (so telling my pylance to chill and don't show error here, its definitely a dictionary)
        validated_data = cast(Dict[str, Any], serializer.validated_data)
        
        query_text = validated_data["query_text"]
        
        products_id_list: list = self.recommendation.search_products(query_text, count)
        
        
        products = Product.objects.filter(id__in = products_id_list)
        
        product_serializer = ProductSerializer(products, many=True)
        
        return Response({
            "status": "success",
            "products": product_serializer.data,
            "total_count": len(product_serializer.data)
        }, status=status.HTTP_200_OK)
        
        
        
        
        