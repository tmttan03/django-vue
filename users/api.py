from django.contrib.auth import logout

from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from .serializers import (
    AuthTokenSerializer,
    UserSerializer,
    RegisterSerializer,
    EmailSerializer,
)

# Had to set an alias because of conflict with
# existing ViewSet named User
from .models import User as UserModel
from utils.mixins import get_object_or_None


class Login(APIView):
    """ user authentication endpoint
    """
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = AuthTokenSerializer

    def post(self, *args, **kwargs):
        """ accepts post data that contains user credentials
            and validates it. Returns a generated token.
        """
        serializer = self.serializer_class(
            data=self.request.data, request=self.request)
        serializer.is_valid(raise_exception=True)

        # TODO: bind the response data to the serializer
        # to make it much cleaner and robust
        return Response({
            'token': serializer.get_token().key,
            'user_id': serializer.user.id
        }, status=200)


class Logout(APIView):
    """
        Logout EndPoint
    """
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        """
           Logout User
        """
        logout(self.request)
        return Response(status=204)


class Register(APIView):
    """ Register endpoint
    """
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response(status=200)
        return Response(serializer.errors, status=400)


class ChangeEmail(APIView):
    """
        User Email EndPoint
    """
    permission_classes = (AllowAny,)

    def put(self, *args, **kwargs):
        """
            Change User Email
        """
        serializer = EmailSerializer(instance=self.request.user,
                                    data=self.request.data,
                                    request=self.request)

        if serializer.is_valid():
            serializer.save()
            return Response(status=204)
        return Response(serializer.errors, status=400)


class Users(ViewSet):
    """ users endpoint
    """
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        users = UserModel.objects.all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data, status=200)


class User(ViewSet):
    """ user endpoint
    """
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    parser_class = (MultiPartParser,)

    def get(self, *args, **kwargs):
        serializer = self.serializer_class(
            instance=self.request.user)
        return Response(serializer.data, status=200)

    def get_current(self, *args, **kwargs):
        user = get_object_or_None(UserModel, id=self.request.GET.get('id'))
        if user:
            serializer = self.serializer_class(instance=user)
            return Response(serializer.data, status=200)
        return Response(status=400)

    def update(self, *args, **kwargs):
        serializer = self.serializer_class(
            data=self.request.data,
            instance=self.request.user)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)




