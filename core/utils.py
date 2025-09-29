# -*- coding: utf-8 -*-
import pdfplumber 
from docx import Document 
import nltk
import logging 
import re 
import requests 
import json 
from typing import Dict, List, Optional 
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
from nltk.corpus import stopwords
import string

logger = logging.getLogger(__name__) 

class CVParser: 
    """RAG destekli CV parser sınıfı - NLTK versiyonu""" 

    def __init__(self): 
        self.patterns = { 
            'phone': r'(\+?90\s?)?(\(?[0-9]{3}\)?[\s.-]?)?[0-9]{3}[\s.-]?[0-9]{2}[\s.-]?[0-9]{2}', 
            'name': r'[A-Z][a-z]+(\s+[A-Z][a-z]+)*$' 
        } 
        self._download_nltk_resources()
        self.stop_words = set(stopwords.words('turkish'))

    def _download_nltk_resources(self):
        """Gerekli NLTK verilerini indirir"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            nltk.download('averaged_perceptron_tagger')
        
        try:
            nltk.data.find('chunkers/maxent_ne_chunker')
        except LookupError:
            nltk.download('maxent_ne_chunker')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        try:
            nltk.data.find('corpora/words')
        except LookupError:
            nltk.download('words')

    def extract_text_from_file(self, dosya_yolu: str) -> Optional[str]:
        """CV dosyasından metin çıkarır"""
        try:
            if dosya_yolu.endswith('.pdf'):
                with pdfplumber.open(dosya_yolu) as pdf:
                    text = ''
                    for page in pdf.pages:
                        text += page.extract_text() or ''
                    return text
            elif dosya_yolu.endswith('.docx'):
                doc = Document(dosya_yolu)
                return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            else:
                logger.error("Desteklenmeyen dosya formatı")
                return None
        except Exception as e:
            logger.error(f"Dosya okuma hatası: {e}")
            return None

    def parse_cv(self, dosya_yolu: str) -> dict:
        """CV dosyasını parse eder"""
        text = self.extract_text_from_file(dosya_yolu)
        if not text:
            return {}

        # RAG benzeri bilgi çıkarma
        veriler = self._extract_basic_info(text)
        veriler.update(self._extract_education(text))
        veriler.update(self._extract_experience(text))
        veriler.update(self._extract_skills(text))

        logger.info(f"CV parse edildi: {dosya_yolu}")
        return veriler

    def _extract_basic_info(self, text: str) -> dict:
        """Temel bilgileri çıkarır"""
        veriler = {}

        # Email
        self.patterns['email'] = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        email_match = re.search(self.patterns['email'], text)
        if email_match:
            veriler['email'] = email_match.group()

        # Telefon
        phone_match = re.search(self.patterns['phone'], text)
        if phone_match:
            veriler['telefon'] = phone_match.group().strip()

        # İsim - NLTK ile geliştirilmiş isim tanıma
        lines = text.split('\n')
        for line in lines[:10]:  # İlk 10 satırda isim ara
            line = line.strip()
            if self._is_likely_name(line):
                parts = line.split()
                if len(parts) >= 2:
                    veriler['ad'] = parts[0]
                    veriler['soyad'] = ' '.join(parts[1:])
                    break

        return veriler

    def _is_likely_name(self, text: str) -> bool:
        """Metnin isim olma olasılığını kontrol eder"""
        if not text or len(text) < 3:
            return False
        
        # Büyük harf kontrolü
        words = text.split()
        if len(words) < 2 or len(words) > 4:
            return False
        
        # Tüm kelimelerin ilk harfi büyük olmalı
        for word in words:
            if not word[0].isupper():
                return False
        
        # Sayı içermemeli
        if any(char.isdigit() for char in text):
            return False
            
        return True

    def _extract_education(self, text: str) -> dict:
        """Eğitim bilgilerini çıkarır"""
        egitim_verileri = {'egitimler': []}

        # Eğitim anahtar kelimeleri
        egitim_keywords = [
            'üniversite', 'universite', 'fakülte', 'fakulte', 'lise',
            'bölüm', 'bolum', 'lisans', 'yüksek lisans', 'yuksek lisans',
            'doktora', 'master', 'öğrenci', 'ogrenci', 'mezun', 'okul'
        ]

        sentences = sent_tokenize(text)
        current_egitim = {}

        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in egitim_keywords):
                # NLTK tokenization ile daha iyi analiz
                words = word_tokenize(sentence)
                tagged_words = pos_tag(words)
                
                # Özel isimleri bul (üniversite isimleri)
                proper_nouns = []
                for word, tag in tagged_words:
                    if tag == 'NNP' and word[0].isupper() and len(word) > 2:
                        proper_nouns.append(word)
                
                if proper_nouns:
                    current_egitim['okul'] = ' '.join(proper_nouns)
                
                # Bölüm bilgisi
                bolum_keywords = ['bölüm', 'bolum', 'department', 'faculty']
                for i, (word, tag) in enumerate(tagged_words):
                    if word.lower() in bolum_keywords and i + 1 < len(tagged_words):
                        next_word = tagged_words[i + 1][0]
                        if next_word[0].isupper():
                            current_egitim['bolum'] = next_word
                            break

                if current_egitim:
                    egitim_verileri['egitimler'].append(current_egitim.copy())
                    current_egitim = {}

        return egitim_verileri

    def _extract_experience(self, text: str) -> dict:
        """İş deneyimi bilgilerini çıkarır"""
        deneyim_verileri = {'is_deneyimleri': []}

        # Deneyim anahtar kelimeleri
        deneyim_keywords = [
            'deneyim', 'tecrübe', 'tecrube', 'iş', 'is', 'çalışma', 'calisma',
            'pozisyon', 'görev', 'gorev', 'şirket', 'sirket', 'firma',
            'company', 'corporation', 'ltd', 'a.ş', 'as'
        ]

        sentences = sent_tokenize(text)
        current_deneyim = {}

        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in deneyim_keywords):
                # Şirket ismi bulma
                words = word_tokenize(sentence)
                tagged_words = pos_tag(words)
                
                # Büyük harfle başlayan ve uzun özel isimler
                company_candidates = []
                for word, tag in tagged_words:
                    if tag == 'NNP' and word[0].isupper() and len(word) > 1:
                        company_candidates.append(word)
                
                if company_candidates:
                    current_deneyim['sirket'] = ' '.join(company_candidates)

                # Pozisyon bilgisi
                pozisyon_keywords = ['pozisyon', 'position', 'görev', 'gorev', 'rol', 'role']
                for i, (word, tag) in enumerate(tagged_words):
                    if word.lower() in pozisyon_keywords:
                        # Sonraki birkaç kelimeyi pozisyon olarak al
                        pozisyon_words = []
                        for j in range(i + 1, min(i + 4, len(tagged_words))):
                            next_word, next_tag = tagged_words[j]
                            if next_tag in ['NN', 'NNP', 'JJ'] and next_word not in string.punctuation:
                                pozisyon_words.append(next_word)
                        if pozisyon_words:
                            current_deneyim['pozisyon'] = ' '.join(pozisyon_words)
                        break

                # Tarih bilgisi
                tarih_patterns = [
                    r'\d{4}[-/]\d{4}',  # 2020-2022
                    r'\d{4}[-/]\s*\d{4}',  # 2020 - 2022
                    r'\d{1,2}[./]\d{4}[-/]\d{1,2}[./]\d{4}'  # 01.2020-12.2022
                ]
                
                for pattern in tarih_patterns:
                    tarih_match = re.search(pattern, sentence)
                    if tarih_match:
                        current_deneyim['baslangic_tarihi'] = tarih_match.group()
                        break

                if current_deneyim:
                    deneyim_verileri['is_deneyimleri'].append(current_deneyim.copy())
                    current_deneyim = {}

        return deneyim_verileri

    def _extract_skills(self, text: str) -> dict:
        """Yetenek bilgilerini çıkarır"""
        skills_verileri = {'yetenekler': []}

        # Programlama dilleri ve teknolojiler
        tech_keywords = [
            'python', 'django', 'javascript', 'react', 'vue', 'angular',
            'java', 'spring', 'c#', '.net', 'php', 'laravel',
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis',
            'docker', 'kubernetes', 'aws', 'azure', 'git',
            'html', 'css', 'bootstrap', 'node.js', 'express',
            'typescript', 'jquery', 'rest', 'api', 'graphql',
            'linux', 'unix', 'windows', 'macos'
        ]

        # Diller
        language_keywords = [
            'türkçe', 'turkce', 'ingilizce', 'almanca', 'fransızca', 'fransizca',
            'ispanyolca', 'italyanca', 'rusça', 'rusca', 'arapça', 'arapca'
        ]

        text_lower = text.lower()
        
        # Teknik yetenekler
        for skill in tech_keywords:
            if skill in text_lower:
                skills_verileri['yetenekler'].append(skill)

        # Dil yetenekleri
        languages_found = []
        for lang in language_keywords:
            if lang in text_lower:
                languages_found.append(lang)
        
        if languages_found:
            skills_verileri['diller'] = languages_found

        # NLTK ile anahtar kelime çıkarımı
        words = word_tokenize(text_lower)
        filtered_words = [word for word in words if word not in self.stop_words and word not in string.punctuation]
        
        # Tekrar eden önemli kelimeleri bul
        from collections import Counter
        word_freq = Counter(filtered_words)
        
        # Sık geçen ve uzun kelimeleri yetenek olarak ekle
        for word, count in word_freq.most_common(20):
            if len(word) > 3 and count > 1 and word not in skills_verileri['yetenekler']:
                # Teknik terim kontrolü
                if any(tech in word for tech in ['script', 'sql', 'db', 'cloud', 'web', 'dev']):
                    skills_verileri['yetenekler'].append(word)

        return skills_verileri

# Global parser instance
cv_parser = CVParser()

def cv_parse_et(dosya_yolu: str) -> dict:
    """CV dosyasından bilgileri çıkarır - Legacy fonksiyon"""
    return cv_parser.parse_cv(dosya_yolu)

def bulk_cv_parse(dosya_yollari: List[str]) -> List[dict]:
    """Toplu CV parse işlemi"""
    sonuclar = []
    for dosya_yolu in dosya_yollari:
        try:
            veri = cv_parser.parse_cv(dosya_yolu)
            veri['dosya_adi'] = dosya_yolu
            sonuclar.append(veri)
        except Exception as e:
            logger.error(f"CV parse hatası {dosya_yolu}: {e}")
            sonuclar.append({'hata': str(e), 'dosya_adi': dosya_yolu})
    return sonuclar