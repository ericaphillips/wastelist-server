from django.core.exceptions import ValidationError
from django.db import models
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from wastelistapi.models import WasteUser
from django.contrib.auth.models import User

class Users(ViewSet):
    def retrieve(self, request, pk=None):
        """Handle GET requests for single User
        Returns: Response -- JSON serialized User instance
        """
        if pk == None:
            waste_user = WasteUser.objects.get(user=request.auth.user)

        else:
            waste_user = WasteUser.objects.get(pk=pk)
        
        serializer = WasteUserSerializer(
            waste_user, context={'request': request})
        
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to User resource
        Returns: Response -- JSON serialized list of users
        """
        
        users = WasteUser.objects.all()

        serializer = WasteUserSerializer(
            users, many=True, context={'request': request}
        )
        return Response(serializer.data)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for Users
    Arguments: Serializer type
    """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')

class WasteUserSerializer(serializers.ModelSerializer):
    """JSON serializer for Waste Users
    Arguments: serializer type
    """
    user = UserSerializer(many=False)

    class Meta:
        model = WasteUser
        fields = ('id', 'user', 'phone', 'zipcode', 'pharmacy')
        depth = 1