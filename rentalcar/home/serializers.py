from rest_framework import serializers
from .models import UserProfile,Vehicle,VehicleImage,ROLE_CHOICES,Bookings
from django.utils import timezone


class RegisterSerializers(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False,allow_blank=True)
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=ROLE_CHOICES)
    phone = serializers.CharField(max_length=15)

    class Meta:
      model = UserProfile
      fields = ['username','email','password','role','phone']


   
class BookingsSerializer(serializers.ModelSerializer):

    total_price = serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)

    class Meta:
     model = Bookings
     fields = ['vehicle','start_date','end_date','total_price']

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        vehicle = data.get('vehicle')

        if end_date <=start_date:
            raise serializers.ValidationError("End date must be after start date")
        
        if start_date < timezone.now().date():
            raise serializers.ValidationError("Cannot booking in the past")
        
        if Bookings.objects.filter(
            vehicle=vehicle,
            start_date__lt=end_date,
            end_date__gt=start_date,
            status__in=['PENDING','CONFIRMED',]
        ).exists():
            raise serializers.ValidationError("Vehicle is already booked for these days")
        
        return data
            

    def create(self,validated_data):

        request = self.context['request']
        user_profile = request.user.userprofile
        vehicle = validated_data['vehicle']

        if vehicle.owner == user_profile:
            raise serializers.ValidationError(
                "Owner cannot book their own vehicle"
            )
        start = validated_data['start_date']
        end = validated_data['end_date']

        days = (end - start).days
        if days == 0:
            days = 1
        
        total_price = days * vehicle.daily_rate

        booking = Bookings.objects.create(
            customer=user_profile,
            total_price=total_price,
            **validated_data
                
        )

        return booking
             



