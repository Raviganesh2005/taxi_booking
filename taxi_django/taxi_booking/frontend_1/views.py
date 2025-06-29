from django.shortcuts import render,redirect
from django.http import HttpResponse

from django.contrib.auth.hashers import make_password,check_password

from django.contrib.auth import authenticate

from django.contrib.sessions.backends.db import SessionStore

from .models import *


from django.http import JsonResponse
import json

from django.db.models import Q,Count

from django.contrib.auth import login as auth_login,logout as auth_logout

from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_protect

from . import backends

import random



# render Home page

def home(request):
    return render(request,"home.html")

# render About page

def about(request):
    return render(request,"aboutus.html")

# render Safety page

def safety(request): 
    return render(request,"safety.html")

# render Careers page

def careers(request):
    return render(request,"careers.html")

# render Contact page

def contact(request):
    return render(request,"contact.html")

# Choose the signup page driver or traveler


def sign(request):

    return render(request,"sign.html")

# render Traveler Signup or Register page 


def signup_traveller(request):
    
    return render(request,"signup.html")

# Get traveler detail for signup and singup page


def getSignupTraveller(request):

    name = request.POST["name"]
    username = request.POST["username"]
    password = request.POST["password"]
    mobile = request.POST["mobile"]
    email = request.POST["email"]
    city = request.POST["address"]

    password = make_password(password) 

    Customer.objects.create(customer_name = name, customer_username = username,customer_password = password,customer_mobile = mobile,customer_email = email,customer_city = city )

    return redirect("http://127.0.0.1:8000/")

# render Signup driver page


def signup_driver(request):


    return render(request,"signup_driver.html")

# Get the details for signup driver

def getSignupDriver(request):

    name = request.POST["name"]
    username = request.POST["username"]
    password = request.POST["password"]
    mobile = request.POST["mobile"]
    email = request.POST["email"]
    city = request.POST["address"]
    licence = request.POST["licence"]
    vehicle = request.POST["vehicle"]

    if (vehicle == "auto"):

        vehicle = Vehicle.objects.get(vehicle_id = 1)

    if (vehicle == "car"):

        vehicle = Vehicle.objects.get(vehicle_id = 2)

    if(vehicle == "bike"):

        vehicle = Vehicle.objects.get(vehicle_id = 3)


    password = make_password(password) 

    Driver.objects.create(driver_name = name, driver_username = username,driver_password = password,driver_mobile = mobile,driver_email = email,driver_city = city,driver_licence = licence,driver_vehicle = vehicle,vehicles = vehicle )

    return redirect("http://127.0.0.1:8000/")


# render traveler or user login page


def login(request):

    return render(request,"login.html")

# User or traveler login 

def login_check(request):
    if request.method == 'POST':
        try:
            # Parse JSON from request body
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # Your authentication logic here
            # ...

            user = authenticate(request,username = username,password = password)


            if user:

                auth_login(request,user)
                request.session['customer_session'] = True
                request.session['user_type'] = 'customer'
    
                return JsonResponse({'success': True, 'redirect': '/booking/'})
            
        
        except json.JSONDecodeError:

            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    # Return 405 for non-POST requests
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# render driver login page

def login_driver(request):

    return render(request,"driver_login.html")

# login driver

def login_driver_check(request):

    if request.method == 'POST':
        try:
            # Parse JSON from request body
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # Your authentication logic here
            # ...

            user = authenticate(request,username = username,password = password)


            if user:

                auth_login(request,user)

                request.session['driver_session'] = True
                request.session['user_type'] = 'driver'


    
                return JsonResponse({'success': True, 'redirect': '/driver_booking/'})   


        
        except json.JSONDecodeError:

            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    # Return 405 for non-POST requests
    return JsonResponse({'error': 'Method not allowed'}, status=405)



# render password forget page
    
    

def forget(reqest):

    return render(reqest,"forget.html")

# Traveler password change

def change_password(request):

    username = request.POST["username"]

    password = request.POST["new_password"]

    password = make_password(password)

    user_get = Customer.objects.filter(customer_username = username).update(customer_password = password)

    print(user_get)

    return redirect("/login/")

# Driver change password

def change_password_driver(request):

    username = request.POST["username"]

    password = request.POST["new_password"]

    password = make_password(password)

    user_get = Driver.objects.filter(driver_username = username).update(driver_password = password)

    print(user_get)

    return redirect("/login/")


# Booking page 

def booking(request):

    user = request.user 

    auto = Vehicle.objects.filter(pk = 1)
    car = Vehicle.objects.filter(pk=2)
    bike = Vehicle.objects.filter(pk=3)

    source =""
    dest=""
    kilometer=0
    auto_fare =0
    bike_fare=0
    car_fare=0

    if request.method == 'POST':


        source = request.POST["source"]
        dest = request.POST["to"]

        print(len(source))

        if (len(source)!=0 and len(dest)!= 0):

            kilometer = random.randrange(1,50)

    farea = Vehicle.objects.filter(pk=1)
    farec = Vehicle.objects.filter(pk=2)
    fareb = Vehicle.objects.filter(pk=3)

    for autof in farea:

        auto_fare = kilometer * autof.vehicle_fare

    for carf in farec:

        car_fare  = kilometer * carf.vehicle_fare

    for bikef in fareb:

        bike_fare = kilometer * bikef.vehicle_fare


    return render(request,"booking.html",{"user":user,'auto':auto,'car':car,'bike':bike,'source':source,'dest':dest,'kilometer':kilometer,'auto_fare':auto_fare,
                                          'bike_fare':bike_fare,'car_fare':car_fare})

# After choose the vehicle and pick and drop,  The booking details page

def booking_details(request,vehicle_id, fare , source =None , dest = None):


    v= Vehicle.objects.filter(vehicle_id = vehicle_id)

    from urllib.parse import unquote

    pickup_location = unquote(source)
    dropoff_location = unquote(dest)

    fare = float(fare)

    pick = pickup_location
    
    drop = dropoff_location

    # Driver.objects.all().update(status = "available")


    return render(request,"Booking_detail.html",{'vehicle':v,'fare':fare,'pick':pick,'drop':drop})

# render Traveler Profile page


def profile(request):

    customer = request.user

    return render(request,"profile.html",{'user':customer})

# We can change Traveler profile, using this page

def edit_profile(request):

    user = request.user

    return render(request,"edit_profile.html",{"user":user})

# traveler Profile edit page

def profile_edit(request):

    name = request.POST["name"]
    username = request.POST["username"]
    mobile = request.POST["mobile"]
    email = request.POST["email"]
    city = request.POST["address"]

    cus = request.user

    cus_id = cus.customer_id



    Customer.objects.filter(customer_id = cus_id ).update(customer_name = name,customer_username = username,customer_mobile = mobile,
                                                          customer_email = email,customer_city = city)


    return redirect("/booking/profile")

# render driver profile page

def driver_profile(request):

    driver = request.user

    return render(request,"driver_profile.html",{'driver':driver})

# Driver profile edit page

def driver_edit_profile(request):

    driver = request.user

    return render(request,"driver_edit_profile.html",{'driver':driver})

# Here Driver profile is changed successfully

def driver_edit_profile_change(request):

    name = request.POST["name"]
    username = request.POST["username"]
    mobile = request.POST["mobile"]
    email = request.POST["email"]
    city = request.POST["address"]

    dri = request.user

    dri_id = dri.driver_id



    Driver.objects.filter(driver_id = dri_id ).update(driver_name = name,driver_username = username,driver_mobile = mobile,
                                                          driver_email = email,driver_city = city)


    return redirect("/driver_booking/profile")

# Logout and end the active session


def logout(request):

    user = request.user

    print(user)

    if (isinstance(user,Driver)):

        Driver.objects.filter(Q(pk = user.driver_id) & Q(driver_username = user.driver_username)).update(status = False)

    if (isinstance(user,Customer)):

        Customer.objects.filter(Q(pk = user.customer_id) & Q(customer_username = user.customer_username))

    auth_logout(request)

    return redirect("/home")


# Here Booking information and drivers are allocated

def booking_status(request,vehicle_id,fare,source=None,dest=None):

    user = request.user


    from urllib.parse import unquote

    pickup_location = unquote(source)
    dropoff_location = unquote(dest)

    fare = float(fare)

    pick = pickup_location
    
    drop = dropoff_location

    drivers = Driver.objects.filter(Q(status = "available") & Q(vehicles__vehicle_id = vehicle_id))


    d = []

    for driver in drivers:

        d.append(driver.driver_id)

    if (len(d)!=0):

        ids = random.choice(d)

        print(ids)


        driver_ins = Driver.objects.get(pk = ids)

        selected_driver = Driver.objects.filter(pk = ids)  

        b = Booking.objects.create(traveller =user,driver = driver_ins ,pickup = pick,destination = drop,fare = fare )

        b.refresh_from_db()


        book = Booking.objects.filter(booking_id = b.booking_id)

        for booking in book:

            print(booking.status)

        return render(request,"booking_status.html",{'fare':fare,'pick':pick,'drop':drop,'driver':selected_driver,'book':book})
    
    else:

        return HttpResponse("<h2>No drivers available</h2>")
    

# Here Receive the driver ride 

def driver_booking(request):

    driver = request.user


    book = Booking.objects.filter(Q(status = "pending") & Q(driver__driver_id = driver.driver_id))

    book_accepted = Booking.objects.filter(Q(status = "accepted") & Q(driver__driver_id = driver.driver_id))

    book_completed = Booking.objects.filter(Q(status = "completed") & Q(driver__driver_id = driver.driver_id))


    return render(request,"driver_booking.html",{'booking':book,'driver':driver,'book_accepted':book_accepted,'book_completed':book_completed})

# Driver accepted page

def accept(request,booking_id,driver_id):

    Booking.objects.filter(pk = booking_id).update(status = "accepted")

    Driver.objects.filter(driver_id = driver_id).update(status = "ride")

    
    return redirect("/driver_booking/")

# Driver cancel the ride

def delete(request,booking_id,driver_id):

    Booking.objects.filter(pk = booking_id).delete()

    return redirect("/driver_booking/")

# Traveler cancel the ride

def delete_traveler(request,booking_id):

    Booking.objects.filter(pk = booking_id).delete()

    return redirect("/booking/")

# Complete the ride

def complete(request,booking_id):

    Booking.objects.filter(booking_id = booking_id).update(status = "completed")

    return redirect("/driver_booking/")

# render Payment page 

def payment_traveler(request,booking_id):

    b=Booking.objects.filter(booking_id = booking_id)
    b.update(status = "complete")

    return render(request,"payment.html",{'book':b})

# cash on completed ride

def payment(request,booking_id):

    book = Booking.objects.filter(booking_id = booking_id)

    for booking in book:

        id = booking.booking_id
        d_id = booking.driver_id
        c_id = booking.traveller_id
        fare = booking.fare

    booking_ins = Booking.objects.get(booking_id = id)
    driver_ins = Driver.objects.get(driver_id = d_id)
    customer_ins = Customer.objects.get(customer_id = c_id)

    Payment.objects.create(booking  = booking_ins, driver = driver_ins,traveler = customer_ins , type = "cash" , amount = fare )



    return render(request,"feedback.html",{'book':book})

# Gpay method

def Gpay(request,booking_id):

    book = Booking.objects.filter(booking_id = booking_id)

    for booking in book:

        d = booking.driver_id
    
    driver = Driver.objects.filter(driver_id = d)

    return render(request,"gpay.html",{'book':book,'driver':driver})

# Payment confirmation gpay

def payment_confirmation(request,booking_id):

    book = Booking.objects.filter(booking_id = booking_id)

    return render(request,"pay.html",{'book':book})

# payment completed

def payment_complete(request,booking_id):

    book = Booking.objects.filter(booking_id = booking_id)

    for booking in book:

        id = booking.booking_id
        d_id = booking.driver_id
        c_id = booking.traveller_id
        fare = booking.fare

    booking_ins = Booking.objects.get(booking_id = id)
    driver_ins = Driver.objects.get(driver_id = d_id)
    customer_ins = Customer.objects.get(customer_id = c_id)

    Payment.objects.create(booking  = booking_ins, driver = driver_ins,traveler = customer_ins , type = "gpay" , amount = fare )

    return render(request,"feedback.html",{'book':book})

# Feedback of the ride
def Feedback(request,booking_id):

    book = Booking.objects.filter(booking_id = booking_id)

    for book in book:

        id = book.booking_id
        d_id = book.driver_id
        c_id = book.traveller_id

    rate = request.POST["rating"]

    comment = request.POST["comment"]

    feedback.objects.create(booking = book , driver_id = d_id,traveler_id = c_id , rating = rate,comment =comment)

    return redirect("/booking/")

# History of driver and Traveler

def driver_history(request):

    user = request.user

    d=0
    c=0

    if (isinstance(user,Driver)):

        booking = Booking.objects.filter(Q(driver__driver_id = user.driver_id) & Q(status = "complete"))

        for book in booking:

                d = book.driver_id

                c = book.traveller_id

        driver = Driver.objects.filter(driver_id = d)

        customer = Customer.objects.filter(customer_id = c)

        return render(request,"history.html",{'booking':booking,'driver':driver,'customer':customer})
    
    if (isinstance(user,Customer)):

          booking = Booking.objects.filter(Q(traveller__customer_id = user.customer_id) & Q(status = "complete"))

          for book in booking:

                d = book.driver_id

                c = book.traveller_id

          driver = Driver.objects.filter(driver_id = d)

          customer = Customer.objects.filter(customer_id = c)

          return render(request,"traveler_history.html",{'booking':booking,'driver':driver,'customer':customer})

    

    


