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

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single pharmacy
        Returns: Response -- JSON serialized pharmacy instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/pharmacies/2
            #
            # The `2` at the end of the route becomes `pk`
            pharmacy = Pharmacy.objects.get(pk=pk)
            serializer = PharmacySerializer(pharmacy, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

class PharmacySerializer(serializers.ModelSerializer):
    """JSON serializer
    Argument:
        serializer type
    """
    class Meta:
        model = Pharmacy
        fields = ('id', 'name', 'address', 'zipcode', 'appointment_hours')
        depth = 1