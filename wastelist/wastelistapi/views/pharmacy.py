from django.core.exceptions import ValidationError
from django.db import models
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from wastelistapi.models import Pharmacy

class Pharmacies(ViewSet):
    # handle POST operations, returns JSON serialized pharmacy instance
    def create(self, request):
        # Create a new Python instance of the class
        # and set its properties from what was sent
        # in the body of the request from the client
        pharmacy = Pharmacy()
        pharmacy.name = request.data['name']
        pharmacy.address = request.data['address']
        pharmacy.zipcode = request.data['zipcode']
        pharmacy.appointment_hours = request.data['appointment_hours']

        # Try to save the new pharmacy to the database
        # Then serialize the instance as JSON
        # And send the JSON as a response to the client request
        try:
            pharmacy.save()
            serializer = PharmacySerializer(pharmacy, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception
        # and send a response with a 400 status code to tell
        # the client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

class PharmacySerializer(serializers.ModelSerializer):
    """JSON serializer
    Argument:
        serializer type
    """
    class Meta:
        model = Pharmacy
        fields = ('id', 'name', 'address', 'zipcode', 'appointment_hours')
        depth = 1