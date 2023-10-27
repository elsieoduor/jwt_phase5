from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
import jwt, datetime
# Create your views here.

class registerview(APIView):
  def post(self, request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
  
class loginview(APIView):
  def post(self, request):
    email = request.data('email')
    password = request.data('password')

    user = User.objects.filter(email=email).first()
    if user is None:
      raise AuthenticationFailed('user not found!')
    
    if not user.check_password(password):
      raise AuthenticationFailed('incorrect password!')
    
    payload ={
      'id':user.id,
      'exp':datetime.datetime.utcnow() + datetime.timedelta(hour=1),
      'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, 'secret', algorithm= 'HS256').decode('utf-8')

    response = Response()
    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {'jwt': token}
    return response
  

class userview(APIView):
  def get(self, request):
    token = request.COOKIES.get('jwt')

    if not token:
      raise AuthenticationFailed('Not authenticated')
    
    try:
      payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('Token expired or invalid')
    
    user = User.objects.filter(id =payload['id']).first()
    serializer = UserSerializer(user)
    return Response(serializer.data)  


class logoutview(APIView):
  def post(self, request):
    response = Response()
    response.delete_cookie('jwt')
    response.data ={
      'message': 'delete successful'
    }
    return response