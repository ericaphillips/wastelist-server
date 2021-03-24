from django.core.exceptions import ValidationError
from django.db import models
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers
from rest_framework import status
from wastelistapi.models import WasteUser, PharmacyCustomer, Message

class Messages(ViewSet):
    # handle POST operations, returns JSON serialized message instance
    def create(self, request):
        # Create a new Python instance of the class
        # and set its properties from what was sent
        # in the body of the request from the client
        message = Message()
        message.sender = request.data['sender']
        message.receiver = request.data['receiver']
        message.content = request.data['content']

        # Try to save the new mesage to the database
        # Then serialize the instance as JSON
        # And send the JSON as a response to the client request
        try:
            message.save()
            serializer = MessageSerializer(message, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception
        # and send a response with a 400 status code to tell
        # the client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single message
        Returns: Response -- JSON serialized message instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/messages/2
            #
            # The `2` at the end of the route becomes `pk`
            message = Message.objects.get(pk=pk)
            serializer = MessageSerializer(message, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to resource
        Returns:
            Response -- JSON serialized list of messages
        """
        # Get all message records from the database
        messages = Message.objects.all()


        # Support filtering by type
        
        serializer = MessageSerializer(
            messages, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
       
        message = Message.objects.get(pk=pk)
        message.sender = request.data['sender']
        message.receiver = request.data['receiver']
        message.content = request.data['content']
        message.save()
        # 204 status send back
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        #Handle DELETE requests/ single message, returns 200, 404, or 500 status code
        try:
            message = Message.objects.get(pk=pk)
            message.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Message.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MessageSerializer(serializers.ModelSerializer):
    """JSON serializer
    Argument:
        serializer type
    """
    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver')
        depth = 1