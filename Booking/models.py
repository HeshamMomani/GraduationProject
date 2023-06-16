import datetime
from django.db import models
from my_users.models import CustomUser
from my_users.models import provider ,Recipient
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField 



    
    
    
'''

    # booked_time=[(models.DateTimeField(),models.DateTimeField())]
    # Add additional fields for the provider's schedule
    #free time 
    #booked_time= models.ManyToManyField('TimeSlot' ,default= ( models.DateTimeField(default=timezone.now),
    #                                                           models.DateTimeField(default=timezone.now)) ) 
    
    """"
class TimeSlot(models.Model):
    #schedule = models.ForeignKey(providerSchedule, on_delete=models.CASCADE, related_name='time_slots')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Time slot for {self.schedule.provider.username} - {self.start_time} to {self.end_time}"   
    
    
    time_slot = TimeSlot(start_time=start_time, end_time=end_time)
time_slot.save()
provider_schedule.booked_time.add(time_slot)
provider_schedule.save()"""
    
if CustomUser.objects.filter(email=eemail).exists():
user = CustomUser.objects.filter(email=eemail)

TIMEBLOCK_CHOICES = (
    ("08:00-09:00", "8:00 AM - 9:00 AM"),
    ("09:00-10:00", "9:00 AM - 10:00 AM"),
    ("10:00-11:00", "10:00 AM - 11:00 AM"),
    ("11:00-12:00", "11:00 AM - 12:00 PM"),
    ("12:00-13:00", "12:00 PM - 1:00 PM"),
    ("13:00-14:00", "1:00 PM - 2:00 PM"),
    ("14:00-15:00", "2:00 PM - 3:00 PM"),
    ("15:00-16:00", "3:00 PM - 4:00 PM"),
    ("16:00-17:00", "4:00 PM - 5:00 PM"),
)
'''

"""
SEVICE_TYPE_CHOICES = (
        ('cleaning ', 'general cleaning'),
        ('gardening ', 'gardening Services '),
        ('dry cleaning', 'carpets and rugs'),
    )
    category = models.CharField(max_length=22, choices=SEVICE_TYPE_CHOICES)
    """

class Service_category(models.Model):
    category = models.CharField(max_length=100,unique=True) 
    #service_Info = models.ForeignKey(service_Info, on_delete=models.CASCADE, related_name=' service  category ')


class service_Info (models.Model):
    #must add a list of service_Info in user (provider)
    provider = models.ForeignKey(provider, on_delete=models.CASCADE, related_name='create_as_provider')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    price = models.IntegerField(default=0)
    category =  models.ForeignKey(Service_category,default=1, on_delete=models.CASCADE, related_name='service_category')
    #ask hesho how react deals with maps  ()'''
    #domain = 'amman'
    
    #pictures =""



class ReservationInfo(models.Model):
    #must add a list of Reservation in user (recipient)
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, related_name='booking_as_recipient')
    service_Info = models.ForeignKey(service_Info, on_delete=models.CASCADE, related_name='create_as_provider')
    start_time  =  models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    #location 
    # date time  ask hesho how react sends date time ?
    def __str__(self):
        return f'Reservation for {self.recipient} - {self.service_Info}'


class providerSchedule(models.Model):
    provider = models.OneToOneField(provider, on_delete=models.CASCADE, related_name='schedule')
    TimeSlot =  models.ManyToManyField('TimeSlot', related_name='schedules')



class TimeSlot(models.Model):
        schedule = models.ForeignKey(providerSchedule, on_delete=models.CASCADE, related_name='time_slots', default=None)
        start_time = models.DateTimeField(default=timezone.now)
        end_time = models.DateTimeField(default=timezone.now)