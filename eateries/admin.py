from django.contrib import admin
from .models import HotelroomBasemodel, hotelroomBooking
from .models import Amenities, BaseModel

admin.site.register(hotelroomBooking)
