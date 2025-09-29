from django.test import TestCase 
from django.contrib.auth.models import User 
from rest_framework.test import APITestCase, APIClient 
from rest_framework import status 
from core.models import IKFirma, MusteriFirma, IKUser, Aday, IsIlanlari 
from django.utils import timezone 
from datetime import timedelta 
 
class ViewTests(APITestCase): 
    def setUp(self): 
        self.client = APIClient() 
        self.ik_firma = IKFirma.objects.create(ad="Test IK") 
        self.musteri_firma = MusteriFirma.objects.create(ad="Test Musteri") 
        self.user = User.objects.create_user(username='testuser', password='testpass123') 
        self.ik_user = IKUser.objects.create(user=self.user, ik_firma=self.ik_firma) 
        self.ik_user.yetkili_musteri_firmalar.add(self.musteri_firma) 
 
    def test_authentication(self): 
        response = self.client.post('/api/token/', { 
            'username': 'testuser', 
            'password': 'testpass123' 
        }) 
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertIn('access', response.data) 
 
    def test_is_ilanlari_list(self): 
        # �nce login ol 
        response = self.client.post('/api/token/', { 
            'username': 'testuser', 
            'password': 'testpass123' 
        }) 
        token = response.data['access'] 
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token) 
 
        # Is ilanı oluştur 
        IsIlanlari.objects.create( 
            ik_firma=self.ik_firma, 
            musteri_firma=self.musteri_firma, 
            baslik="Test Ilan", 
            aciklama="Test Aciklama", 
            kapanis_tarihi=timezone.now() + timedelta(days=30) 
        ) 
 
        response = self.client.get('/api/is-ilanlari/') 
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
 
    def test_aday_list(self): 
        response = self.client.post('/api/token/', { 
            'username': 'testuser', 
            'password': 'testpass123' 
        }) 
        token = response.data['access'] 
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token) 
 
        Aday.objects.create(ad="Test", soyad="Aday", email="test@aday.com") 
        response = self.client.get('/api/adaylar/') 
        self.assertEqual(response.status_code, status.HTTP_200_OK) 

from datetime import datetime, timedelta 
