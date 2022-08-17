from rest_framework import serializers
from .models import *
import jwt

class LoginSerializer(serializers.Serializer):
    source_code = serializers.CharField(max_length=1000)


    def validate(self, data):
        source_code = data.get('source_code', None)

        # Raise an exception if an
        # source_code is not provided.
        if source_code is None:
            raise serializers.ValidationError(
                'An Source code paramter required.'
            )

        return {
            'source_code': self.decode(source_code)
        }
    
    def decode(self, token):
        return jwt.decode(token, "secret", algorithms="HS256")