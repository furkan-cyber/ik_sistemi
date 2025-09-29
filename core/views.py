from rest_framework import viewsets, permissions, status 
from rest_framework.decorators import action 
from rest_framework.response import Response 
from django_filters.rest_framework import DjangoFilterBackend 
from .models import IKFirma, MusteriFirma, IKUser, Aday, IsIlanlari, Egitim, IsDeneyimi, AdayAkis, Aktivite, Statu 
from .serializers import * 
from .permissions import * 
from .utils import bulk_cv_parse, cv_parse_et 
import logging 
import os 
from django.core.files.storage import default_storage 
from django.core.files.base import ContentFile 
 
logger = logging.getLogger(__name__) 
 
class IsIlanlariViewSet(viewsets.ModelViewSet): 
    queryset = IsIlanlari.objects.all() 
    serializer_class = IsIlanlariSerializer 
    permission_classes = [permissions.IsAuthenticated, IsIlanlariPermission] 
    filter_backends = [DjangoFilterBackend] 
    filterset_fields = ['musteri_firma', 'statu'] 
 
    def perform_create(self, serializer): 
        serializer.save() 
        logger.info(f"Yeni iş ilanı oluşturuldu: {serializer.instance}") 
 
class AdayViewSet(viewsets.ModelViewSet): 
    queryset = Aday.objects.all() 
    serializer_class = AdaySerializer 
    permission_classes = [permissions.IsAuthenticated] 
    filter_backends = [DjangoFilterBackend] 
    filterset_fields = ['ad', 'soyad', 'email'] 
 
    @action(detail=False, methods=['post']) 
    def bulk_upload(self, request): 
        """Toplu CV yükleme ve parse işlemi""" 
        try: 
            uploaded_files = request.FILES.getlist('cv_files') 
            if not uploaded_files: 
                return Response( 
                    {"error": "Dosya bulunamadı"}, 
                    status=status.HTTP_400_BAD_REQUEST 
                ) 
 
            # Dosyalar� ge�ici olarak kaydet 
            dosya_yollari = [] 
            for uploaded_file in uploaded_files: 
                # Dosya uzant�s� kontrol� 
                if not uploaded_file.name.lower().endswith(('.pdf', '.docx')): 
                    continue 
 
                # Dosyay� kaydet 
                file_path = default_storage.save( 
                    f'temp_cv/{uploaded_file.name}', 
                    ContentFile(uploaded_file.read()) 
                ) 
                dosya_yollari.append(file_path) 
 
            # CV'leri parse et 
            parse_sonuclari = bulk_cv_parse(dosya_yollari) 
 
            # Adaylar� olu�tur 
            olusturulan_adaylar = [] 
            for sonuc in parse_sonuclari: 
                if 'hata' not in sonuc: 
                    try: 
                        # Aday olu�tur 
                        aday_data = { 
                            'ad': sonuc.get('ad', ''), 
                            'soyad': sonuc.get('soyad', ''), 
                            'email': sonuc.get('email', ''), 
                            'telefon': sonuc.get('telefon', '') 
                        } 
 
                        # Email kontrol� 
                        if aday_data['email']: 
                            aday, created = Aday.objects.get_or_create( 
                                email=aday_data['email'], 
                                defaults=aday_data 
                            ) 
 
                            if created: 
                                # E�itim bilgilerini ekle 
                                for egitim in sonuc.get('egitimler', []): 
                                    Egitim.objects.create( 
                                        aday=aday, 
                                        okul=egitim.get('okul', ''), 
                                        bolum=egitim.get('bolum', '') 
                                    ) 
 
                                # �� deneyimlerini ekle 
                                for deneyim in sonuc.get('is_deneyimleri', []): 
                                    IsDeneyimi.objects.create( 
                                        aday=aday, 
                                        sirket=deneyim.get('sirket', ''), 
                                        pozisyon=deneyim.get('pozisyon', '') 
                                    ) 
 
                                olusturulan_adaylar.append({ 
                                    'id': aday.id, 
                                    'ad': aday.ad, 
                                    'soyad': aday.soyad, 
                                    'email': aday.email, 
                                    'durum': 'olu�turuldu' 
                                }) 
                            else: 
                                olusturulan_adaylar.append({ 
                                    'id': aday.id, 
                                    'ad': aday.ad, 
                                    'soyad': aday.soyad, 
                                    'email': aday.email, 
                                    'durum': 'zaten mevcut' 
                                }) 
 
                    except Exception as e: 
                        logger.error(f"Aday oluşturma hatası: {e}") 
                        olusturulan_adaylar.append({ 
                            'hata': str(e), 
                            'dosya': sonuc.get('dosya_adi', '') 
                        }) 
 
            # Ge�ici dosyalar� temizle 
            for dosya_yolu in dosya_yollari: 
                try: 
                    default_storage.delete(dosya_yolu) 
                except: 
                    pass 
 
            logger.info(f"Toplu CV yükleme tamamlandı: {len(olusturulan_adaylar)} aday işlendi") 
            return Response({ 
                'message': f'{len(uploaded_files)} dosya işlendi', 
                'olusturulan_adaylar': olusturulan_adaylar, 
                'toplam': len(olusturulan_adaylar) 
            }) 
 
        except Exception as e: 
            logger.error(f"Toplu CV yükleme hatası: {e}") 
            return Response( 
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR 
            ) 
 
class AdayAkisViewSet(viewsets.ModelViewSet): 
    queryset = AdayAkis.objects.all() 
    serializer_class = AdayAkisSerializer 
    permission_classes = [permissions.IsAuthenticated, AdayAkisPermission] 
    filter_backends = [DjangoFilterBackend] 
    filterset_fields = ['is_ilani', 'aday'] 
 
    @action(detail=True, methods=['post']) 
    def aktivite_ekle(self, request, pk=None): 
        aday_akis = self.get_object() 
        serializer = AktiviteSerializer(data=request.data) 
        if serializer.is_valid(): 
            serializer.save( 
                aday_akis=aday_akis, 
                ik_kullanici=request.user, 
                ik_firma=request.user.ikuser.ik_firma 
            ) 
            logger.info(f"Yeni aktivite eklendi: {serializer.instance}") 
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
