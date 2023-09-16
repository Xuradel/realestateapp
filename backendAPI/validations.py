from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework import permissions

UserModel = get_user_model()

def custom_validation(data):
    email = data['email'].strip()
    username = data['username'].strip()
    password = data['password'].strip()
    ##
    if not email or UserModel.objects.filter(email=email).exists():
        raise ValidationError('choose another email')
    ##
    if not password or len(password) < 8:
        raise ValidationError('choose another password, min 8 characters')
    ##
    if not username:
        raise ValidationError('choose another username')
    return data


def validate_email(data):
    email = data['email'].strip()
    if not email:
        raise ValidationError('an email is needed')
    return True

def validate_username(data):
    username = data['username'].strip()
    if not username:
        raise ValidationError('choose another username')
    return True

def validate_password(data):
    password = data['password'].strip()
    if not password:
        raise ValidationError('a password is needed')
    return True

from rest_framework import permissions

class ReadOnlyOrAuthenticatedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow unauthenticated users to perform read-only actions (e.g., GET)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Require authentication for other actions (e.g., POST, PUT, DELETE)
        return request.user and request.user.is_authenticated
