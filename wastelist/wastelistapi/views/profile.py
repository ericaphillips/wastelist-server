"""View module for handling requests about user's pharmacy list"""
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from wastelistapi.models import WasteUser, Pharmacy, PharmacyCustomer


class Profile(ViewSet):
    """Customer can see profile information"""

    def list(self, request):
        """Handle GET requests to profile resource

        Returns:
            Response -- JSON representation of user info and pharmacies
        """
        customer = WasteUser.objects.get(user=request.auth.user)
        customer.pharmacies = Pharmacy.objects.filter(pharmacycustomers__customer=customer)

        
        serializer = CustomerSerializer(
            customer, many=False, context={'request': request})

        
        

        return Response(serializer.data)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for customer's related Django user"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

class PharmacySerializer(serializers.ModelSerializer):
    """JSON serializer for pharmacies"""

    class Meta:
        model = Pharmacy
        fields = ('id', 'name', 'address', 'zipcode', 'appointment_hours', 'customers')

class CustomerSerializer(serializers.ModelSerializer):
    """JSON serializer for customers"""
    user = UserSerializer(many=False)
    pharmacies = PharmacySerializer(many=True)

    class Meta:
        model = WasteUser
        fields = ('user', 'phone', 'zipcode', 'pharmacies')
