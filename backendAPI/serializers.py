from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from .models import building
import django_filters

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = '__all__'
	def create(self, clean_data):
		user_obj = UserModel.objects.create_user(email=clean_data['email'], password=clean_data['password'])
		user_obj.username = clean_data['username']
		user_obj.save()
		return user_obj

class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
	##
	def check_user(self, clean_data):
		user = authenticate(username=clean_data['email'], password=clean_data['password'])
		if not user:
			raise ValidationError('user not found')
		return user

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ('email', 'username')

class BuildingFilter(django_filters.FilterSet):
    price__gte = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    price__lte = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    bedrooms__gte = django_filters.NumberFilter(field_name="bedrooms", lookup_expr='gte')
    bathrooms__gte = django_filters.NumberFilter(field_name="bathrooms", lookup_expr='gte')
    state = django_filters.CharFilter(field_name="state", lookup_expr='icontains')
    city = django_filters.CharFilter(field_name="city", lookup_expr='icontains')
    class Meta:
        model = building
        fields = ['price__gte', 'price__lte', 'bedrooms__gte', 'bathrooms__gte', 'state', 'city']

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = building
        fields = '__all__'