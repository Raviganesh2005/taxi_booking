from django.db import models

from django.contrib.auth.models import User, Group, Permission
from django.contrib import admin
from django.utils import timezone





class Customer(models.Model):

    customer_id = models.BigAutoField(primary_key= True)

    customer_name = models.CharField(max_length=200,null = False)

    customer_username = models.CharField(max_length=200,null=False)

    customer_password = models.CharField(max_length=200,unique= True,null= False)

    customer_city = models.CharField(max_length=200)

    customer_mobile =  models.CharField(max_length=200,unique= True)

    customer_email = models.EmailField(max_length=200, unique= True)

    last_login = models.CharField(max_length=200,default=0)

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default = False)

    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, blank=True, related_name="customer_groups")
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name="customer_permissions")

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def get_username(self):
        return self.customer_username



    def __str__(self):
         return self.customer_username


    def is_authenticated(self):
        return True  # For authenticated users
    
    @property
    def is_anonymous(self):
        return False  # Authenticated users are not anonymous

    def __str__(self):
        return self.customer_username

    
class Vehicle(models.Model):

        vehicle_id = models.BigAutoField(primary_key=True)

        vehicle_name = models.CharField(max_length=100)

        vehicle_fare = models.DecimalField(default=0,max_digits=10,decimal_places=2)

        def __str__(self):
             
             return self.vehicle_name
        


class Driver(models.Model):

        vehicle = {
            "auto":"auto",
            "car":"car",
            "bike":"bike",
        }

        status = {
             
             'available':'available',
             'ride':'ride',
             'active':'active'
        }


        driver_id = models.BigAutoField(primary_key= True)

        vehicles = models.ForeignKey(Vehicle,on_delete=models.CASCADE)

        driver_name = models.CharField(max_length=200,null = False)

        driver_username = models.CharField(max_length=200,null=False)

        driver_password = models.CharField(max_length=200,unique= True,null= False)

        driver_city = models.CharField(max_length=200)

        driver_mobile =  models.CharField(max_length=200,unique= True)

        driver_email = models.EmailField(max_length=200,unique= True)

        driver_vehicle = models.CharField(max_length=200,choices=vehicle)

        driver_licence = models.CharField(max_length=200, unique=True,default=0)

        last_login = models.CharField(max_length=200,default=0)

        is_active = models.BooleanField(default= True)

        status = models.CharField(max_length=200,choices=status,default='available')


        def __str__(self):
             return self.driver_username
        


        


class Booking(models.Model):
     
     status = {
          
          'pending':'pending',
          'accepted':'accepted',
          'cancel':'cancel',
          'completed':'completed',
     }
     
     booking_id = models.BigAutoField(primary_key= True)

     traveller = models.ForeignKey(Customer,on_delete=models.CASCADE)

     driver = models.ForeignKey(Driver,on_delete=models.CASCADE)

     pickup = models.CharField(max_length=200)

     destination = models.CharField(max_length=200)

     booking_date = models.DateTimeField(auto_now_add=True)

     fare = models.DecimalField(decimal_places=2,max_digits=10)

     status = models.CharField(max_length=200,choices=status,default='pending')


class Payment(models.Model):

     type = {
          'cash':'cash',
          'gpay':'gpay',
     }

     payment_id = models.BigAutoField(primary_key= True)

     booking = models.ForeignKey(Booking,on_delete=models.CASCADE)

     driver = models.ForeignKey(Driver,on_delete=models.CASCADE)

     traveler = models.ForeignKey(Customer,on_delete=models.CASCADE)

     type = models.CharField(max_length=200,choices=type)

     amount = models.CharField(max_length=200)

     date = models.DateTimeField(auto_now_add=True)



class feedback(models.Model):
     
     feedback_id = models.BigAutoField(primary_key= True)

     booking = models.ForeignKey(Booking,on_delete=models.CASCADE)

     driver_id = models.IntegerField()

     traveler_id = models.IntegerField()

     rating = models.CharField(max_length=100)

     comment = models.CharField(max_length=500)





      




    


    


