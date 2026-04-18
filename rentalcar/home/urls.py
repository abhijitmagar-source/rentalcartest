from django.urls import path
from .views import Register,Booking,Login,Home


urlpatterns = [
    path('register/',Register.as_view(),name='register'),
    path('login/', Login.as_view()),
    path('booking/',Booking.as_view(),name='booking'),
    path('',Home.as_view(),name='home')

]