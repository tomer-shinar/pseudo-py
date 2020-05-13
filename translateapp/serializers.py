from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from .models import AppUser, VerificationCode
import datetime


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppUser
        fields = ('username', 'email', 'status')


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # todo email verification
        verification_code = VerificationCode(code=0, expiration=datetime.datetime.now())
        verification_code.save()
        instance = self.Meta.model(verification_code=verification_code, status="verified", **validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = AppUser
        fields = ('token', 'username', 'password', 'email', 'status')
