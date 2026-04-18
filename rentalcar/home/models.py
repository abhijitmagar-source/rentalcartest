from django.db import models
from django.conf import settings

ROLE_CHOICES = (

    ('OWNER' ,'Owner'),
    ('CUSTOMER' , 'Customer'),
)
CAR_CHOICES =(

    ('SEDAN','Sedan'),
    ('HATCHBACK','Hatchback'),
    ('SUV','Suv')
)
BOOKING_STATUS = (
    ('PENDING', 'Pending'),
    ('CONFIRMED', 'Confirmed'),
    ('CANCELLED', 'Cancelled'),
    ('COMPLETED', 'Completed'),
)

# MODEL_CHICES = (

#     ('SWIFT DEZIRE','Swift Dezire'),
#     ('SWIFT WAGNOR', 'Swift Wagnor'),
#     ('SWIFT ERTIGA','Swift Ertiga')
# )

class BaseModel(models.Model):
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    role  = models.CharField(max_length=10,choices=ROLE_CHOICES)
    phone = models.CharField(max_length=10,unique=True)

    def __str__(self):
        return self.role
    
class Vehicle(BaseModel):
    owner = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    title = models.CharField( max_length=50)
    description = models.TextField()
    city = models.CharField(max_length=10)
    location = models.CharField(max_length=230)
    vehicle_type = models.CharField( max_length=50, choices=CAR_CHOICES)
    model = models.CharField( max_length=50)
    make = models.CharField(max_length=40)
    hourly_rate = models.DecimalField(max_digits=10,decimal_places=2)
    daily_rate = models.DecimalField(max_digits=10,decimal_places=2)
    weekly_rate = models.DecimalField(max_digits=10,decimal_places=2)
    is_active = models.BooleanField(default=True)

class VehicleImage(BaseModel):
    vehicle = models.ForeignKey(Vehicle ,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='vehicle_images/')


class Bookings(BaseModel):
    vehicle = models.ForeignKey(Vehicle,on_delete=models.CASCADE)
    customer = models.ForeignKey(UserProfile,on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()

    total_price = models.DecimalField(max_digits=10,decimal_places=2)

    status = models.CharField(max_length=20,choices=BOOKING_STATUS)

    is_paid = models.BooleanField(default=False)
    pickup_location = models.CharField(max_length=255)
    drop_location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.customer.user.username} - {self.vehicle.title}"
