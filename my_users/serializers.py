from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from .models import CustomUser


class CustomUserSerializer (serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def validate(self, attrs):
        eemail = attrs.get('email', '')
        if CustomUser.objects.filter(email=eemail).exists():
            raise serializers.ValidationError(
                {'email': ('email is taken')})
        return super().validate(attrs)

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


'''

        '''

class logiserilazier (serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def login(self,email,password):
        email = email
        password = password

        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                return user
            else:
                raise serializers.ValidationError({'password': ('Invalid password.')})
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'email': ('Invalid email.')})
    """ 
    def validate(self, attrs):
        eemail = attrs.get('email', '')
        password = attrs.get('password')
        user = None
        if CustomUser.objects.filter(email=eemail) :
            user = CustomUser.objects.get(email=eemail).first()
            if user.check_password(password):
                return attrs
            else : raise serializers.ValidationError(
                {'email': ('pass is wrong')})
        else:raise serializers.ValidationError(
                {'email': ('email is wrong')})
    
"""

