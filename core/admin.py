from django.contrib import admin 
from .models import IKFirma, MusteriFirma, IKUser, Aday, IsIlanlari, Egitim, IsDeneyimi, AdayAkis, Aktivite, Statu 
 
@admin.register(IKFirma) 
class IKFirmaAdmin(admin.ModelAdmin): 
    list_display = ['ad', 'created_at'] 
 
@admin.register(MusteriFirma) 
class MusteriFirmaAdmin(admin.ModelAdmin): 
    list_display = ['ad', 'sektor', 'created_at'] 
 
@admin.register(IKUser) 
class IKUserAdmin(admin.ModelAdmin): 
    list_display = ['user', 'ik_firma', 'created_at'] 
 
@admin.register(Aday) 
class AdayAdmin(admin.ModelAdmin): 
    list_display = ['ad', 'soyad', 'email', 'created_at'] 
 
@admin.register(IsIlanlari) 
class IsIlanlariAdmin(admin.ModelAdmin): 
    list_display = ['baslik', 'musteri_firma', 'ik_firma', 'statu', 'kapanis_tarihi'] 
    list_filter = ['statu', 'ik_firma', 'musteri_firma'] 
 
admin.site.register(Egitim) 
admin.site.register(IsDeneyimi) 
admin.site.register(AdayAkis) 
admin.site.register(Aktivite) 
admin.site.register(Statu) 
