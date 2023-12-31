from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password
from rest_framework import generics
from .models import building
from .serializers import BuildingSerializer, BuildingFilter
from .validations import ReadOnlyOrAuthenticatedPermission


class BuildingView(generics.ListCreateAPIView):
		queryset = building.objects.all()
		serializer_class = BuildingSerializer
		ordering_fields = ['title', 'location', 'price']
		# filter_backends = [DjangoFilterBackend]  # Use DjangoFilterBackend for filtering
		filterset_class = BuildingFilter  # Use the custom filter class
		search_fields = ['title', 'location', 'price']
		permission_classes = [ReadOnlyOrAuthenticatedPermission]  # Apply the custom permission class



class BuildingSingleView(generics.RetrieveUpdateDestroyAPIView):
		queryset = building.objects.all()
		serializer_class = BuildingSerializer
		permission_classes = [ReadOnlyOrAuthenticatedPermission]  # Apply the custom permission class


class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)
	def post(self, request):
		clean_data = custom_validation(request.data)
		serializer = UserRegisterSerializer(data=clean_data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.create(clean_data)
			if user:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)
	##
	def post(self, request):
		data = request.data
		assert validate_email(data)
		assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			login(request, user)
			return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)


class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)
	##
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)


