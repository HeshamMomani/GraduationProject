import jwt
from rest_framework import authentication,exceptions
from django.conf import settings

class JWTauth(authentication.BaseAuthentication):
    def authenticate(self, request):
        authdata = authentication.get_authorization_header(request)
        if not authdata:
            return None
        prefix,token=authdata.decode('utf-8').split(' ')
        try:
            payload = jwt.decode(token,settings.
            JWT_SECRET_KEY)

 

        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed('token invalid')
        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.AuthenticationFailed('ExpiredSignatureError')  
        return super().authenticate(request)