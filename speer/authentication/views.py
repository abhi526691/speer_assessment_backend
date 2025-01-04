from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import signupSerializer
from django.contrib.auth.models import User
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class signupAPI(APIView):
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = signupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User Created Successfully",
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class loginAPI(APIView):
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                return Response({
                    "error": "Invalid Credentials."
                }, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)
            return Response({
                "user_id": user.id,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                "error": "Invalid Credentials."
            }, status=status.HTTP_401_UNAUTHORIZED)
