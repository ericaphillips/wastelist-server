import json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from wastelistapi.models import WasteUser, Pharmacy


@csrf_exempt
def login_user(request):
    '''Handles the authentication of a wastelist user

    Method arguments:
      request -- The full HTTP request object
    '''

    req_body = json.loads(request.body.decode())

    # If the request is a HTTP POST, get relevant info
    if request.method == 'POST':

        # Use the built-in authentication method to verify
        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)
        
        # If authentication was successful, respond with their token
        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            waste_user = WasteUser.objects.get(user=authenticated_user)
            pharmacist = False

            if waste_user.pharmacy is not None:
                pharmacist = True

            data = json.dumps({"valid": True, "token": token.key, "pharmacist": pharmacist})
            return HttpResponse(data, content_type='application/json')

        else:
            # Bad login details provided, can't log the user in.
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')


@csrf_exempt
def register_user(request):
    '''Handles the creation of a new wastelist user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Load the JSON string of the request body into a dict
    req_body = json.loads(request.body.decode())

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    new_user = User.objects.create_user(
        username=req_body['username'],
        email=req_body['email'],
        password=req_body['password'],
        first_name=req_body['first_name'],
        last_name=req_body['last_name']
    )

    # Now save the extra info in the wastelistapi_wasteuser table
    wasteUser = WasteUser.objects.create(
        phone=req_body['phone'],
        zipcode=req_body['zipcode'],
        # pharmacy=req_body['pharmacy'],
        user=new_user
    )

    # Commit the user to the database by saving it
    wasteUser.save()

    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=new_user)
    pharmacist = False

    # Return the token to the client
    data = json.dumps({"token": token.key, "pharmacist": pharmacist})
    return HttpResponse(data, content_type='application/json')