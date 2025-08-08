from datetime import timedelta
from typing import Any, cast

from django.contrib.auth import authenticate
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken

from account.utils import LoginSupport

from .._serializers import LoginSerializer
from ._base import BaseAPIView, Response, api_exception_handler, status


class LoginAPI(BaseAPIView):
    """
    API class to help user to login, and obtain JWT access and refresh tokens.
    """
    log_sup = LoginSupport()
    
    @api_exception_handler
    @log_sup.login_limiter(wrong_attempts_allowed=5, period=timedelta(days=1))
    def post(self, request):
        
        attempts_left = self.log_sup.attempts_left(request)
        serializer = LoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "failed",
                "message": serializer.errors,
                "attempts_left": attempts_left,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        
        # I have checked for None type above (so telling my pylance to chill and don't show error here, its definitely a dictionary)
        validated_data = cast(dict[str, Any], serializer.validated_data)
        
        user = authenticate(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        

        if user:
            refresh = RefreshToken.for_user(user=user)

            # Reset if password is correct
            cache.set(key=self.log_sup.cache_key, value=[])
            
            return Response({
                "status":"success",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
            
        return Response({
            "status": "failed",
            "detail_for_user":f"Username or Password is Incorrect, {attempts_left} {"attempts" if attempts_left>1 else "attempt"} left",
        }, status=status.HTTP_401_UNAUTHORIZED)