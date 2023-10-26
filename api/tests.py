from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Restaurant


class RestaurantViewSetTestCase(APITestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)


        self.restaurant_data = {'name': 'Test Restaurant'}
        self.restaurant = Restaurant.objects.create(**self.restaurant_data)

    def test_get_restaurant_list(self):
        url = '/api/restaurants/' 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)  

    def test_create_restaurant(self):
        url = '/api/restaurants/'
        new_restaurant_data = {'name': 'New Restaurant'}

        response = self.client.post(url, data=new_restaurant_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        self.assertEqual(Restaurant.objects.count(), 2) 
        self.assertEqual(Restaurant.objects.get(id=2).name, 'New Restaurant')

    def test_update_restaurant(self):
        url = f'/api/restaurants/{self.restaurant.id}/'
        updated_data = {'name': 'Updated Restaurant'}

        response = self.client.put(url, data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        self.restaurant.refresh_from_db() 
        self.assertEqual(self.restaurant.name, 'Updated Restaurant')

    def test_get_single_restaurant(self):
        url = f'/api/restaurants/{self.restaurant.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Restaurant')
