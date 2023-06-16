from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser , provider ,Recipient
# Register your models here.
class CustomUserAdmin (UserAdmin):
    filter_horizontal=()
    list_filter= ()
    fieldsets=()
    list_display = ('id','email','username','password',
                    'usertype','first_name','last_name'
                    ,'is_active','is_admin','is_superuser')
admin.site.register(CustomUser,CustomUserAdmin)    

class providerAdmin (UserAdmin):
    filter_horizontal=()
    list_filter= ()
    fieldsets=()
    list_display = ('id','email','username','password',
                    'usertype','first_name','last_name'
                    ,'is_active','is_admin','is_superuser','age')
admin.site.register(provider,providerAdmin)   

class recipientAdmin (UserAdmin):
    filter_horizontal=()
    list_filter= ()
    fieldsets=()
    list_display = ('id','email','username','password',
                    'usertype','first_name','last_name'
                    ,'is_active','is_admin','is_superuser')
admin.site.register(Recipient,recipientAdmin) 