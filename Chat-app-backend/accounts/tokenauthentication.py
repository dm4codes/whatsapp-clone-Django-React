from .models import User
import jwt
from jwt .exceptions import InvalidTokenError , ExpiredSignatureError
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings 
from django.contrib.auth import get_user_model 
from datetime import datetime , timedelta
from channels.db import database_sync_to_async





class JWTAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        token = self.extract_token(request=request)
        if token is None:
            return None
        try:
            payload = jwt.decode(token , key= settings.SECRET_KEY, algorithms="HS256")
            self.verify_token(payload=payload)
            user_id = payload['id']
            user = User.objects.get(user_id=user_id)
            return user
        except (InvalidTokenError, ExpiredSignatureError , User.DoesNotExist):
            raise AuthenticationFailed("Invalid token")
    
    
    
    def verify_token(self,payload):
        if "exp" not in payload:
            raise InvalidTokenError("Token has no exp")
        
        exp_timestamp = payload['exp']
        current_timestamp = datetime.utcnow().timestamp()
    
        print("exp:" , exp_timestamp)
        print("current_timestamp:" , current_timestamp)
        
        
        if current_timestamp > exp_timestamp:
            raise ExpiredSignatureError("Token expired")
    
    
    # bearer samjdgsdhfgasyjtfiworo23ur8`237`3jrh
    def extract_token(self,request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            print("Token is ....",auth_header.split(' ')[1])
            return auth_header.split(" ")[1]
        return None
    
    
    @database_sync_to_async
    def authenticate_websocket(self , scope , token):
        try:
            payload = jwt.decode(token , key= settings.SECRET_KEY, algorithms="HS256")
            self.verify_token(payload=payload)
            user_id = payload['id']
            user = User.objects.get(user_id=user_id)
            return user
        except (InvalidTokenError, ExpiredSignatureError , User.DoesNotExist):
            raise AuthenticationFailed("Invalid token")
            
               
    
    @staticmethod # this would be same for every object that we create 
    def generate_token(payload):
        expiration = datetime.utcnow() + timedelta(hours=24) # we are adding 24 hours
        payload['exp'] = expiration #creating one mre key in pyload because payload is a dictionary
        print("PALoad is ..............", payload)
        token = jwt.encode(payload=payload, key= settings.SECRET_KEY , algorithm="HS256")
        return token
    
    