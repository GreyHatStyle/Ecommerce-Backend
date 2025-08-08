from django.db.models import Count, F, Q

from shopping.models import Product, UserProductReview

from ..throttles import BurstRateThrottle, SustainedRateThrottle
from ._base import AllowAny, BaseAPIView, Response, status


# TODO: Apply pagenation in future (instead sending count in url)
class HomeProductsAPI(BaseAPIView):
    """
    API to get the most liked products for the home page
    """
    permission_classes = [AllowAny]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]
    
    
    def get(self, request, count: int):

        products = Product.objects.annotate(
            likes=Count('user_review', filter=Q(user_review__reaction='LIKE')),
            dislikes=Count('user_review', filter=Q(user_review__reaction='DISLIKE')),
            net_rating=F('likes') - F('dislikes')
        ).order_by('-net_rating')[:count]
        
        product_data : list[dict] = []
        for product in products:
            
            # Send the user's reaction if provided access token in header
            user_review = None
            if request.user.is_authenticated:
                try:
                    reaction = UserProductReview.objects.get(
                        user=request.user, 
                        product=product
                    )
                    user_review = reaction.reaction
                except UserProductReview.DoesNotExist:
                    user_review = None
            
            product_data.append({
                "id": str(product.id),
                "title": product.title,
                "description": product.description,
                "price": str(product.price),
                "stock": product.stock,
                "image_url": product.image_url,
                "like_count": product.like_count,  
                "dislike_count": product.dislike_count,  
                "net_likes": product.net_likes, 
                "auth_user_review": user_review,
            })
        
        return Response({
            "status": "success",
            "products": product_data,
            "total_count": len(product_data)
        }, status=status.HTTP_200_OK)

