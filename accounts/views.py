from django.shortcuts import render
from rest_framework import authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LoginSerializer
import jwt

class verificationAPI(APIView):

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        decoded_data = serializer.validated_data['source_code']
        return Response({
            'customer_data': decoded_data
        }, 200)


