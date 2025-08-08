from rest_framework.permissions import IsAuthenticated

from account.models import UserAddress

from .._serializers.address_serializer import (CreateAddressSerializer,
                                               UserAddressSerializer)
from ._base import (BaseAPIView, Request, Response, api_exception_handler,
                    status)


class UserAddressAPI(BaseAPIView):
    """
    API to manage user addresses - create, list, update, delete
    """
    permission_classes = [IsAuthenticated]
    
    @api_exception_handler
    def get(self, request: Request) -> Response:
        """
        Get all addresses for the authenticated user
        """
        
        addresses = UserAddress.objects.filter(user=request.user).order_by('-created_at')
        serializer = UserAddressSerializer(addresses, many=True)
        
        return Response({
            "status": "success",
            "addresses": serializer.data,
            "total_addresses": len(serializer.data)
        }, status=status.HTTP_200_OK)
    
    
    # ======================================================================
    
    @api_exception_handler
    def post(self, request: Request) -> Response:
        """
        Create a new address for the authenticated user
        """
        
        serializer = CreateAddressSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "failed",
                "errors": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create address with the authenticated user
        address = serializer.save(user=request.user)
        
        response_serializer = UserAddressSerializer(address)
        
        return Response({
            "status": "success",
            "message": "Address created successfully",
            "address": response_serializer.data
        }, status=status.HTTP_201_CREATED)

