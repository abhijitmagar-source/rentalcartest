from django.contrib import admin
from .models import UserProfile,Vehicle,VehicleImage,Bookings

admin.site.register(UserProfile)
admin.site.register(Vehicle)
admin.site.register(VehicleImage)
admin.site.register(Bookings)