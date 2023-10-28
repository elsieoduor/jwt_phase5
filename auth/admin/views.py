from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import AdminSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import Admin
import jwt, datetime
# Create your views here.

class registerview(APIView):
  def post(self, request):
    serializer = AdminSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
  
class loginview(APIView):
  def post(self, request):
    email = request.data['email']
    password = request.data['password']

    admin = Admin.objects.filter(email=email).first()
    if admin is None:
      raise AuthenticationFailed('user not found!')
    
    if not admin.check_password(password):
      raise AuthenticationFailed('incorrect password!')
    
    payload ={
      'id':admin.id,
      'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
      'iat': datetime.datetime.utcnow()
    }

    # token = jwt.encode(payload, 'secret', algorithm= 'HS256').decode('utf-8')
    token_bytes = jwt.encode(payload, 'secret', algorithm='HS256')
    if isinstance(token_bytes, bytes):
          token = token_bytes.decode('utf-8')
    else:
          # Handle the case where token_bytes is not bytes (e.g., already a string)
          token = token_bytes

    response = Response()
    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {'jwt': token}
    return response
  

class adminview(APIView):
  def get(self, request):
    token = request.COOKIES.get('jwt')

    if not token:
      raise AuthenticationFailed('Not authenticated')
    
    try:
      payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('Token expired or invalid')
    
    admin = Admin.objects.filter(id =payload['id']).first()
    serializer = AdminSerializer(admin)
    return Response(serializer.data)  


class logoutview(APIView):
  def post(self, request):
    response = Response()
    response.delete_cookie('jwt')
    response.data ={
      'message': 'delete successful'
    }
    return response