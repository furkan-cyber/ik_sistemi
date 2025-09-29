from rest_framework import serializers 
from .models import IKFirma, MusteriFirma, IKUser, Aday, IsIlanlari, Egitim, IsDeneyimi, AdayAkis, Aktivite, Statu 
 
class IKFirmaSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = IKFirma 
        fields = '__all__' 
 
class MusteriFirmaSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = MusteriFirma 
        fields = '__all__' 
 
class IsIlanlariSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = IsIlanlari 
        fields = '__all__' 
 
class EgitimSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Egitim 
        fields = '__all__' 
 
class IsDeneyimiSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = IsDeneyimi 
        fields = '__all__' 
 
class AdaySerializer(serializers.ModelSerializer): 
    egitimler = EgitimSerializer(many=True, read_only=True) 
    is_deneyimleri = IsDeneyimiSerializer(many=True, read_only=True) 
 
    class Meta: 
        model = Aday 
        fields = '__all__' 
 
class AdayAkisSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = AdayAkis 
        fields = '__all__' 
 
class AktiviteSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Aktivite 
        fields = '__all__' 
