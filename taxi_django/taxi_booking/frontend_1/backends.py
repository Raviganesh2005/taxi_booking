from .models import *

from django.utils import timezone

from django.contrib.auth.hashers import check_password

class CustomUserAuthBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user =Customer.objects.get(customer_username=username)
 
            if check_password(password, user.customer_password):
                user.last_login = timezone.now()  # Update last_login
                user.save()
                return user
            return None
            

        except Customer.DoesNotExist:
            return None

        

    def get_user(self, user_id):
        try:
            return Customer.objects.get(pk=user_id)
        except Customer.DoesNotExist:
            return None
        
   

