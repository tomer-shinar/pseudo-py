import environ
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from .models import AppUser, VerificationCode
import datetime
from django.utils import timezone


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
        verification_code = self.send_email_verification(validated_data["email"])
        instance = self.Meta.model(verification_code=verification_code, status=AppUser.APPROVED, **validated_data) #todo change status
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    @staticmethod
    def send_email_verification(email):
        """
        send email verification for user
        :param email: the user email
        :return: the verification code for the user
        """
        env = environ.Env()
        environ.Env.read_env()
        frontend_url = env('FRONTEND_URL')
        token = get_random_string(length=32)

        verify_link = frontend_url + '/email-verify/' + token
        subject, from_email, password, to = 'Verify Your Email', env("EMAIL"), env("EMAIL_PASSWORD"), email
        html_content = render_to_string('translateapp/verify_email.html', {'verify_link': verify_link})
        text_content = strip_tags(html_content)

        connection = get_connection(username=from_email, password=password)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        connection.send_messages([msg])

        verification_code = VerificationCode(code=token, expiration=datetime.datetime.now(tz=timezone.utc) +
                                                                    datetime.timedelta(1))
        verification_code.save()
        return verification_code

    class Meta:
        model = AppUser
        fields = ('token', 'username', 'password', 'email', 'status')
