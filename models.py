from django.db import models
from django.contrib.auth.models import User
from django.db import models
import uuid



class BaseModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4  , editable=False, unique=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True




class Amenities(BaseModel):
    amenity_name=models.CharField(max_length=100)

    def __Str__(self) -> str:
        return self.amenity_name


class HotelroomBasemodel(models.Model):
    hotelroom_name= models.CharField(max_length=100)
    hotelroom_price = models.IntegerField()
    description = models.TextField
    amenities=models.ManyToManyField(Amenities)
    room_count=models.IntegerField(default=10)
    images=models.ImageField()
    
    def __str__(self) -> str:
        return self.amenity_name


class hotelroomBooking(BaseModel):
    hotelroom = models.ForeignKey(HotelroomBasemodel , related_name ="hotelroom_booking",on_delete=models.CASCADE  )
    user = models.ForeignKey(User, related_name="user_booking" , on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    booking_type = models.CharField(max_length=100, choices=(('Pre Paid' , 'Pre Paid') , ('Post Paid' , 'Post Paid')))
                                    

# Create your models here.
