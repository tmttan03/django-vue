import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from .models import User


class AuthTokenSerializer(serializers.Serializer):
    """ auth token serializer
    """
    user = None

    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        return super(AuthTokenSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        """ validate email credentials
        """
        email, password = data.values()

        if not email or not password:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        self.user = authenticate(request=self.request, email=email, password=password)

        login(self.request, self.user)

        if not self.user:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        return data

    def get_token(self):
        """ get or generate a user token that is valid for
            `settings.AUTH_TOKEN_EXPIRY_TIME`
        """
        if not self.user:
            msg = _('Unable to login with provided credentials.')
            raise serializers.ValidationError(msg, code="authorization")

        token, created = Token.objects.get_or_create(user=self.user)
        expiry_date = token.created + datetime.timedelta(days=settings.AUTH_TOKEN_EXPIRY_TIME)

        if not created and expiry_date < timezone.now():
            # delete token
            token.delete()
            # generate a new one
            token = Token.objects.create(user=self.user)
        return token


class ShortUserSerializer(serializers.ModelSerializer):
    """ user serializer with only basic
        information.
    """
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'full_name',
        )

    def get_full_name(self, instance):
        """ return the complete name of
            the user.
        """
        return instance.get_full_name()


class UserSerializer(serializers.ModelSerializer):
    """ user serializer
    """
    has_usable_pass = serializers.SerializerMethodField(read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'full_name',
            'has_usable_pass',
            'date_joined',
            'date_updated',
        )

    def __init__(self, *args, **kwargs):
        return super(UserSerializer, self).__init__(*args, **kwargs)

    def get_has_usable_pass(self, instance):
        return instance.has_usable_password()

    def get_full_name(self, instance):
        """ return the complete name of
            the user.
        """
        return instance.get_full_name()


class PasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=False)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        return super(PasswordSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        """
            validates data to check user credentials
        """

        if self.request.user.has_usable_password():
            old_password, new_password, confirm_new_password = data.values()
            if not self.request.user.check_password(old_password):
                raise serializers.ValidationError(_("Wrong old password."), code="authorization")
        else:
            new_password, confirm_new_password = data.values()

        if new_password != confirm_new_password:
            raise serializers.ValidationError(_("Passwords do not match."), code="authorization")

        return data

    def validate_new_password(self, value):
        """
            validates inputed password if accepted by used django password verification
        """
        validate_password(value)
        return value

    def create(self, validated_data):
        """
            set new password for user
        """
        self.request.user.set_password(validated_data.get("new_password"))
        self.request.user.save()
        return self.request.user


class EmailSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message="This email is already exist!"
        )])

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        return super(EmailSerializer, self).__init__(*args, **kwargs)

    def update(self, instance, validated_data):
        """
            set new email for user
        """
        email = validated_data.pop('email', None)
        if email is not None:
            instance.email = email
        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    """user register serializer
    """

    user = None

    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message="This email is already exist!"
        )])

    username = serializers.CharField(
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='This username is already taken.'
        )]
    )

    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'confirm_password',
        )

    def validate(self, data):
        """
            validates data to check user credentials
        """
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError(_("Passwords do not match."), code="authorization")

        return data

    def create(self, validated_data):
        user = User(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
            )
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = '__all__'