from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.db import models


""""
        user = provider.objects.create_user()
        if usertype == 'provider' :
            pass
        if usertype == 'recipient' :    
            pass
        """

'''
this was working 
user = self.model(email=email, username=username, usertype=usertype,
                                first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user
        '''

""""
debuging
email = self.normalize_email(email)
return user
return user
"""

class providerManager(BaseUserManager):

    def create_user(self,email,first_name,last_name,username,usertype, password=None):
        # Create and save a regular user with the given email and password
            email = self.normalize_email(email)
            user = self.model(email=email, username=username, usertype=usertype,
                                first_name=first_name, last_name=last_name)
            user.save(using=self._db)
            return user

class RecipientManager(BaseUserManager):

    def create_user(self,email,first_name,last_name,username,usertype, password=None):
        # Create and save a regular user with the given email and password
            email = self.normalize_email(email)
            user = self.model(email=email, username=username, usertype=usertype,
                                first_name=first_name, last_name=last_name)
            user.save(using=self._db)
            return user
            

class CustomUserManager(BaseUserManager):

    def create_user(self,email,first_name,last_name,username,usertype, password=None):
        # Create and save a regular user with the given email and password
        

        if usertype == 'provider' :
            user = provider.objects.create_user(email=email, username=username, usertype=usertype,
                                first_name=first_name, last_name=last_name)
            
        if usertype == 'recipient' :    
            user = Recipient.objects.create_user(email=email, username=username, usertype=usertype,
                                first_name=first_name, last_name=last_name)

        user.set_password(password)        
        user.save(using=self._db)        
        return user    
        #raise ValueError()

    def create_superuser(self,email,username ,password=None):
        '''
        if not email:
            raise ValueError("The Email field must be set")
        if self.model.objects.filter(email=email).exists():
            raise ValueError('this email already exists')
        '''
        email=self.normalize_email(email)
        user = self.model(email=email,username=username, usertype='admin')
        user.set_password(password)
        
        user.is_admin= True
        user.is_staff= True
        user.is_superuser= True
        user.save(using=self._db)
        return user
    

class CustomUser(AbstractBaseUser):
    USERTYPE_CHOICES = (
        ('provider', 'Service Provider'),
        ('recipient', 'Service Recipient'),
        ('admin', 'Administrator'),
    )
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True,max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    usertype = models.CharField(max_length=22,choices = USERTYPE_CHOICES)#,null=False
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username' # must be unique pk 
    REQUIRED_FIELDS = ['email'] # when creating a super user 

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    

class provider (CustomUser):
    
    #freetime 
    #provider_services = []
    age = models.IntegerField(default=0)
    experience_years = models.IntegerField(default=0)
    experience_details = models.CharField(max_length=255)
        #rating 
        #active_file 
        #location
    objects = providerManager()
    
    
class Recipient (CustomUser):
    booked_Reservation =[]
    objects = RecipientManager()
    #rating 