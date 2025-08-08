from rest_framework.permissions import IsAuthenticated

from shopping.models import Product, UserProductReview

from ..throttles import BurstRateThrottle, SustainedRateThrottle
from ._base import BaseAPIView, Response, status


class ProductReviewAPI(BaseAPIView):
    """
    API to handle user likes/dislikes on products
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]
    
    def post(self, request):
        reaction_type = request.data.get('reaction')
        product_id = request.data.get("product_id")
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({
                "status": "failed",
                "message": "Product not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        if reaction_type not in ['LIKE', 'DISLIKE']:
            return Response({
                "status": "failed",
                "message": "Invalid reaction. Must be LIKE or DISLIKE"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create or update reaction
        reaction, created = UserProductReview.objects.update_or_create(
            user=request.user,
            product=product,
            reaction=reaction_type,
        )
        
        return Response({
            "status": "success",
            "message": f"Product {'liked' if reaction_type == 'LIKE' else 'disliked'} successfully",
            "reaction": reaction.reaction,
            "created": created
        }, status=status.HTTP_200_OK)
    
    def delete(self, request, product_id):
        """Remove user's reaction"""
        try:
            reaction = UserProductReview.objects.get(
                user=request.user,
                product_id=product_id
            )
            reaction.delete()
            return Response({
                "status": "success",
                "message": "Reaction removed successfully"
            }, status=status.HTTP_200_OK)
        except UserProductReview.DoesNotExist:
            return Response({
                "status": "failed",
                "message": "No reaction found"
            }, status=status.HTTP_404_NOT_FOUND)