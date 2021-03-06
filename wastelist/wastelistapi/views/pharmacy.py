from io import SEEK_END
from django.core.exceptions import ValidationError
from django.db import models
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers
from rest_framework import status
from wastelistapi.models import Pharmacy, WasteUser, PharmacyCustomer, pharmacy
from django.contrib.auth.models import User


class Pharmacies(ViewSet):
    # handle POST operations, returns JSON serialized pharmacy instance
    def create(self, request):
        # Create a new Python instance of the class (object instance)
        # Assigning properties of values
        # and set its properties from what was sent
        # in the body of the request from the client
        pharmacy = Pharmacy()
        pharmacy.name = request.data['name']
        pharmacy.address = request.data['address']
        pharmacy.zipcode = request.data['zipcode']
        pharmacy.appointment_hours = request.data['appointment_hours']

        # Try to save the new pharmacy to the database
        # Then serialize the instance as JSON
        # And send the JSON as a response to the client request (line 34)
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
            pharmacy.customers = WasteUser.objects.filter(pharmacycustomers__pharmacy=pharmacy)

            serializer = PharmacyCustomerSerializer(pharmacy, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to resource
        Returns:
            Response -- JSON serialized list of pharmacies
        """
        # Get all pharmacy records from the database
        pharmacies = Pharmacy.objects.all()


        # Support filtering by type
        
        serializer = PharmacySerializer(
            pharmacies, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
       
        pharmacy = Pharmacy.objects.get(pk=pk)
        pharmacy.name = request.data['name']
        pharmacy.address = request.data['address']
        pharmacy.zipcode = request.data['zipcode']
        pharmacy.appointment_hours = request.data['appointment_hours']
        pharmacy.save()
        # 204 status send back
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        #Handle DELETE requests/ single pharmacy, returns 200, 404, or 500 status code
        try:
            pharmacy = Pharmacy.objects.get(pk=pk)
            pharmacy.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Pharmacy.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post', 'delete'], detail=True)
    def modifyCustomers(self, request, pk=None):
        """Managing customers selecting and deselecting pharmacies"""

        # A user wants add a pharmacy to their list
        if request.method == "POST":
            
            pharmacy = Pharmacy.objects.get(pk=pk)

            # Django uses the `Authorization` header to determine
            # which user is making the request
            customer = WasteUser.objects.get(user = request.auth.user)

            try:
                # Determine if the customer is already signed up
                adding = PharmacyCustomer.objects.get(
                    pharmacy=pharmacy, customer=customer)
                return Response(
                    {'message': 'You have already selected this pharmacy'},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            except PharmacyCustomer.DoesNotExist:
                # The user is not signed up.
                adding = PharmacyCustomer()
                adding.pharmacy = pharmacy
                adding.customer = customer
                adding.save()

                return Response({}, status=status.HTTP_201_CREATED)

        # Customer wants to un-select pharmacy from their list
        elif request.method == "DELETE":
            # Handle the case if the client specifies a pharmacy that doesn't exist
            try:
                pharmacy = Pharmacy.objects.get(pk=pk)
                
            except Pharmacy.DoesNotExist:
                return Response(
                    {'message': 'Pharmacy does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            customer = WasteUser.objects.get(user=request.auth.user)

            try:
                # Try to delete the signup
                adding = PharmacyCustomer.objects.get(
                    pharmacy=pharmacy, customer=customer)
                adding.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)

            except PharmacyCustomer.DoesNotExist:
                return Response(
                    {'message': 'Not currently signed up for this pharmacy'},
                    status=status.HTTP_404_NOT_FOUND
                )
        # If the client performs a request with a method of
        # anything other than POST or DELETE, tell client that
        # the method is not supported
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=['get'], detail=False)
    def pharmacist(self, request, pk=None):
        if request.method == "GET":

            myPharmacy = self.request.query_params.get('myPharmacy', None)
            if myPharmacy == "true":
                user = WasteUser.objects.get(user=request.auth.user)
                pharmacyId = user.pharmacy_id
                pharmacy = Pharmacy.objects.get(id=pharmacyId)
                pharmacy.customers = []
                
                serializer = PharmacySerializer(
                pharmacy, many=False, context={'request': request})
                return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def pharmacyCustomers(self, request, pk=None):
        if request.method == "GET":

            myPharmacyCustomers = self.request.query_params.get('myPharmacyCustomers', None)
            if myPharmacyCustomers == "true":
                user = WasteUser.objects.get(user=request.auth.user)
                pharmacyId = user.pharmacy_id
                pharmacy = Pharmacy.objects.get(id=pharmacyId)
                pharmacy.customers = WasteUser.objects.filter(pharmacycustomers__pharmacy=pharmacy)
                
                serializer = PharmacyCustomerSerializer(
                pharmacy, many=False, context={'request': request})
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
        

class PharmacySerializer(serializers.ModelSerializer):
    """JSON serializer
    Argument:
        serializer type
    """

    class Meta:
        model = Pharmacy
        fields = ('id', 'name', 'address', 'zipcode', 'appointment_hours', 'customers')
        depth = 1

class PharmacyCustomerSerializer(serializers.ModelSerializer):
    """JSON serializer
    Argument:
        serializer type
    """
    customers = WasteUserSerializer(many=True)

    class Meta:
        model = Pharmacy
        fields = ('id', 'name', 'address', 'zipcode', 'appointment_hours', 'customers')
        depth = 2