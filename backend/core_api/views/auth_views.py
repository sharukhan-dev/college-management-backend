from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """
    API endpoint for user login.
    Authenticates user credentials and generates an authentication token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        
        user = authenticate(username=username, password=password)
        
        if user:
            # Log the user in and generate a token
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_type': user.user_type})
        else:
            return Response({'error': 'Invalid credentials'}, status=400)


class LogoutView(APIView):
    """
    API endpoint for user logout.
    Invalidates the authentication token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'success': 'Logged Out'})
