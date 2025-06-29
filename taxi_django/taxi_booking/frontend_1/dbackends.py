from .models import *

from django.utils import timezone

from django.contrib.auth.hashers import check_password

class CustomDriverAuthBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            driver =Driver.objects.get(driver_username=username)
 
            if check_password(password, driver.driver_password):
                driver.last_login = timezone.now()  # Update last_login
                driver.save()
                return driver
            return None
            

        except Driver.DoesNotExist:
            return None

        

    def get_user(self, user_id):
        try:
            return Driver.objects.get(pk=user_id)
        except Driver.DoesNotExist:
            return None
        
   

