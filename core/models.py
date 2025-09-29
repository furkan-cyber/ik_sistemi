from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class IKFirma(models.Model):
    ad = models.CharField(max_length=200)
    aciklama = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ad

class MusteriFirma(models.Model):
    ad = models.CharField(max_length=200)
    sektor = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ad

class IKUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ik_firma = models.ForeignKey(IKFirma, on_delete=models.CASCADE)
    yetkili_musteri_firmalar = models.ManyToManyField(MusteriFirma)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.ik_firma.ad}"

class Aday(models.Model):
    ad = models.CharField(max_length=100)
    soyad = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefon = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ad} {self.soyad}"

class Egitim(models.Model):
    aday = models.ForeignKey(Aday, on_delete=models.CASCADE, related_name='egitimler')
    okul = models.CharField(max_length=200)
    bolum = models.CharField(max_length=200)
    baslangic_tarihi = models.DateField()
    bitis_tarihi = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.okul} - {self.bolum}"

class IsDeneyimi(models.Model):
    aday = models.ForeignKey(Aday, on_delete=models.CASCADE, related_name='is_deneyimleri')
    sirket = models.CharField(max_length=200)
    pozisyon = models.CharField(max_length=200)
    baslangic_tarihi = models.DateField()
    bitis_tarihi = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.sirket} - {self.pozisyon}"

class IsIlanlari(models.Model):
    STATU_CHOICES = [
        ('aktif', 'Aktif'),
        ('pasif', 'Pasif'),
    ]

    ik_firma = models.ForeignKey(IKFirma, on_delete=models.CASCADE)
    musteri_firma = models.ForeignKey(MusteriFirma, on_delete=models.CASCADE)
    baslik = models.CharField(max_length=200)
    aciklama = models.TextField()
    kapanis_tarihi = models.DateTimeField()
    statu = models.CharField(max_length=10, choices=STATU_CHOICES, default='aktif')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.baslik} - {self.musteri_firma.ad}"

class AdayAkis(models.Model):
    is_ilani = models.ForeignKey(IsIlanlari, on_delete=models.CASCADE)
    aday = models.ForeignKey(Aday, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.aday} - {self.is_ilani}"

class Statu(models.Model):
    ad = models.CharField(max_length=100)
    aciklama = models.TextField(blank=True)

    def __str__(self):
        return self.ad

class Aktivite(models.Model):
    AKTIVITE_TIPLERI = [
        ('telefon', 'Telefon Araması Yapıldı'),
        ('mail', 'Mail Gönderildi'),
        ('test', 'Test Gönderildi'),
    ]

    aday_akis = models.ForeignKey(AdayAkis, on_delete=models.CASCADE, related_name='aktiviteler')
    aktivite_tipi = models.CharField(max_length=20, choices=AKTIVITE_TIPLERI)
    statu = models.ForeignKey(Statu, on_delete=models.CASCADE)
    aciklama = models.TextField(blank=True)
    ik_kullanici = models.ForeignKey(User, on_delete=models.CASCADE)
    ik_firma = models.ForeignKey(IKFirma, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.aktivite_tipi} - {self.statu.ad}"