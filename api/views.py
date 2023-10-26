from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt.tokens import RefreshToken
from api.renderers import UserRenderer
from api.models import Restaurant, Menu, Vote
from api.serializers import (
 SendPasswordResetEmailSerializer,
 UserChangePasswordSerializer, 
 UserLoginSerializer, 
 UserPasswordResetSerializer, 
 UserProfileSerializer, 
 UserRegistrationSerializer, 
 RestaurantSerializer, 
 MenuSerializer, 
 VoteSerializer
 )


class RestaurantViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        restaurants=None
        pk=request.query_params.get('id')
        if pk is not None:
            restaurants =self.get_object(pk=pk)
            serializer = RestaurantSerializer(restaurants)
            return Response(serializer.data)
        
        paginator = LimitOffsetPagination()
        result_set = paginator.paginate_queryset(Restaurant.objects.all(), request)
        serializer = RestaurantSerializer(result_set, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        print(request)
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get_object(self, pk):
        try:
            return Restaurant.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            return None
    def put(self, request, pk):
        restaurant = self.get_object(pk)
        if restaurant is None:
            return Response("Restaurant not found", status=status.HTTP_404_NOT_FOUND)
        serializer = RestaurantSerializer(restaurant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    def delete(self, request, pk):
        restaurant = self.get_object(pk)
        if restaurant is None:
            return Response("Restaurant not found", status=status.HTTP_404_NOT_FOUND)
        restaurant.delete()
        return Response("Restaurant deleted", status=status.HTTP_204_NO_CONTENT)

class MenuViewSet(APIView):
    def get_object(self, pk):
        try:
            return Menu.objects.get(pk=pk)
        except Menu.DoesNotExist:
            return None
        
    def get(self, request):
        menus=None
        pk=request.query_params.get('id')
        if pk is not None:
           menus = self.get_object(pk=pk)
           serializer = MenuSerializer(menus)
           return Response(serializer.data)
        
        date = request.query_params.get('date')
        if date is not None:
            menus = Menu.objects.filter(date=date)
            serializer = MenuSerializer(menus)
            return Response(serializer.data)

        paginator = LimitOffsetPagination()
        result_set = paginator.paginate_queryset(Menu.objects.all(), request)
        serializer = MenuSerializer(result_set, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = MenuSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        menu = self.get_object(pk)
        if menu is None:
            return Response("Menu not found", status=status.HTTP_404_NOT_FOUND)
        serializer = MenuSerializer(menu, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        menu = self.get_object(pk)
        if menu is None:
            return Response("Menu not found", status=status.HTTP_404_NOT_FOUND)
        menu.delete()
        return Response("Menu deleted", status=status.HTTP_204_NO_CONTENT)
      
class VoteViewSet(APIView):
    def get_object(self, pk):
        try:
            return Vote.objects.get(pk=pk)
        except Vote.DoesNotExist:
            return None
        
    def get(self, request):
        votes=None
        pk=request.query_params.get('id')
        if pk is not None:
           votes = self.get_object(pk=pk)
           serializer = VoteSerializer(votes)
           return Response(serializer.data)
        
        date = request.query_params.get('date')
        if date is not None:
            votes = Vote.objects.filter(date=date)
            serializer = VoteSerializer(votes)
            return Response(serializer.data)

        paginator = LimitOffsetPagination()
        result_set = paginator.paginate_queryset(Vote.objects.all(), request)
        serializer = MenuSerializer(result_set, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        vote = self.get_object(pk)
        if vote is None:
            return Response("Vote not found", status=status.HTTP_404_NOT_FOUND)
        serializer = VoteSerializer(vote, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        vote = self.get_object(pk)
        if vote is None:
            return Response("Vote not found", status=status.HTTP_404_NOT_FOUND)
        vote.delete()
        return Response("Vote deleted", status=status.HTTP_204_NO_CONTENT)
    


# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
   
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    isLogin = authenticate(email=user.email, password=user.password)
    print(isLogin)
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    print(user)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)


    
