from django.test import TestCase 
from django.contrib.auth.models import User 
from core.models import IKFirma, MusteriFirma, IKUser, Aday, IsIlanlari, Egitim, IsDeneyimi, AdayAkis, Aktivite, Statu 
from django.utils import timezone 
from datetime import datetime, timedelta 
 
class ModelTests(TestCase): 
    def setUp(self): 
        self.ik_firma = IKFirma.objects.create(ad="Test IK Şirketi", aciklama="Test açıklama") 
        self.musteri_firma = MusteriFirma.objects.create(ad="Test Müşteri", sektor="Teknoloji") 
        self.user = User.objects.create_user(username='testuser', password='testpass123') 
        self.ik_user = IKUser.objects.create(user=self.user, ik_firma=self.ik_firma) 
        self.ik_user.yetkili_musteri_firmalar.add(self.musteri_firma) 
 
    def test_ik_firma_creation(self): 
        self.assertEqual(str(self.ik_firma), "Test IK Şirketi") 
        self.assertEqual(self.ik_firma.aciklama, "Test açıklama") 
 
    def test_musteri_firma_creation(self): 
        self.assertEqual(str(self.musteri_firma), "Test Müşteri") 
        self.assertEqual(self.musteri_firma.sektor, "Teknoloji") 
 
    def test_ik_user_creation(self): 
        self.assertEqual(str(self.ik_user), "testuser - Test IK Şirketi") 
        self.assertEqual(self.ik_user.ik_firma, self.ik_firma) 
 
    def test_aday_creation(self): 
        aday = Aday.objects.create( 
            ad="Ahmet", 
            soyad="Yılmaz", 
            email="ahmet@test.com", 
            telefon="05551234567" 
        ) 
        self.assertEqual(str(aday), "Ahmet Yılmaz") 
        self.assertEqual(aday.email, "ahmet@test.com") 
 
    def test_is_ilani_creation(self): 
        is_ilani = IsIlanlari.objects.create( 
            ik_firma=self.ik_firma, 
            musteri_firma=self.musteri_firma, 
            baslik="Backend Developer", 
            aciklama="Python Django geliştirici aranıyor", 
            kapanis_tarihi=timezone.now() + timedelta(days=30) 
        ) 
        self.assertEqual(str(is_ilani), "Backend Developer - Test Müşteri") 
        self.assertEqual(is_ilani.statu, "aktif") 
 
    def test_egitim_creation(self): 
        aday = Aday.objects.create(ad="Mehmet", soyad="Demir", email="mehmet@test.com") 
        egitim = Egitim.objects.create( 
            aday=aday, 
            okul="İstanbul Teknik Üniversitesi", 
            bolum="Bilgisayar Mühendisliği", 
            baslangic_tarihi=datetime(2018, 9, 1), 
            bitis_tarihi=datetime(2022, 6, 1) 
        ) 
        self.assertEqual(str(egitim), "İstanbul Teknik Üniversitesi - Bilgisayar Mühendisliği") 
 
    def test_is_deneyimi_creation(self): 
        aday = Aday.objects.create(ad="Ayşe", soyad="Kaya", email="ayse@test.com") 
        is_deneyimi = IsDeneyimi.objects.create( 
            aday=aday, 
            sirket="ABC Teknoloji", 
            pozisyon="Yazılım Geliştirici", 
            baslangic_tarihi=datetime(2022, 1, 1), 
            bitis_tarihi=datetime(2023, 12, 31) 
        ) 
        self.assertEqual(str(is_deneyimi), "ABC Teknoloji - Yazılım Geliştirici") 

    def test_aktivite_creation(self): 
        aday = Aday.objects.create(ad="Ali", soyad="Şahin", email="ali@test.com") 
        is_ilani = IsIlanlari.objects.create( 
            ik_firma=self.ik_firma, 
            musteri_firma=self.musteri_firma, 
            baslik="Frontend Developer", 
            aciklama="React geliştirici aranıyor", 
            kapanis_tarihi=timezone.now() + timedelta(days=15) 
        ) 
        aday_akis = AdayAkis.objects.create(aday=aday, is_ilani=is_ilani) 
        statu = Statu.objects.create(ad="Olumlu", aciklama="Aday olumlu yanıt verdi") 
        aktivite = Aktivite.objects.create( 
            aday_akis=aday_akis, 
            aktivite_tipi="telefon", 
            statu=statu, 
            ik_kullanici=self.user, 
            ik_firma=self.ik_firma, 
            aciklama="Aday ile telefon görüşmesi yapıldı" 
        ) 
        self.assertEqual(str(aktivite), "telefon - Olumlu") 
