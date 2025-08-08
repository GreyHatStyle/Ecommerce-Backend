from rest_framework.permissions import IsAuthenticated

from account.models import UserAddress

from .._serializers.address_serializer import (CreateAddressSerializer,
                                               UserAddressSerializer)
from ._base import (BaseAPIView, Request, Response, api_exception_handler,
                    status)


class UserAddressManageAPI(BaseAPIView):
    """
    API to manage individual address - get, update, delete
    """
    permission_classes = [IsAuthenticated]
    
    def get_address(self, user, address_id):
        """Helper method to get address for the user"""
        try:
            return UserAddress.objects.get(id=address_id, user=user)
        except UserAddress.DoesNotExist:
            return None
    
    # ============================================================================
    
    @api_exception_handler
    def get(self, request: Request, address_id: str) -> Response:
        """
        Get specific address by ID
        """
        
        address = self.get_address(request.user, address_id)
        
        if not address:
            return Response({
                "status": "failed",
                "message": "Address not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserAddressSerializer(address)
        
        return Response({
            "status": "success",
            "address": serializer.data
        }, status=status.HTTP_200_OK)
    
    # ============================================================================
    
    @api_exception_handler
    def put(self, request: Request, address_id: str) -> Response:
        """
        Update specific address
        """
        
        address = self.get_address(request.user, address_id)
        
        if not address:
            return Response({
                "status": "failed",
                "message": "Address not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CreateAddressSerializer(address, data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response({
                "status": "failed",
                "errors": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        updated_address = serializer.save()
        response_serializer = UserAddressSerializer(updated_address)
        
        return Response({
            "status": "success",
            "message": "Address updated successfully",
            "address": response_serializer.data
        }, status=status.HTTP_200_OK)
    
    
    # ============================================================================
    
    
    @api_exception_handler
    def delete(self, request: Request, address_id: str) -> Response:
        """
        Delete specific address
        """
        
        address = self.get_address(request.user, address_id)
        
        if not address:
            return Response({
                "status": "failed",
                "message": "Address not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        address.delete()
        
        return Response({
            "status": "success",
            "message": "Address deleted successfully"
        }, status=status.HTTP_200_OK)