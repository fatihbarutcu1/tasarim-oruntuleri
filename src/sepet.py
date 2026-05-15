from abc import ABC, abstractmethod

class Urun:
    def __init__(self, ad: str, fiyat: float):
        self.ad = ad
        self.fiyat = fiyat

class Indirim(ABC):
    @abstractmethod
    def hesapla(self, brut_toplam: float, urun_sayisi: int) -> float:
        pass

class YuzdeIndirimi(Indirim):
    def hesapla(self, brut_toplam: float, urun_sayisi: int) -> float:
        return brut_toplam * 0.90  

class KuponIndirimi(Indirim):
    def __init__(self, kupon_kodu: str):
        self.kupon_kodu = kupon_kodu

    def hesapla(self, brut_toplam: float, urun_sayisi: int) -> float:
        if self.kupon_kodu == "INDIRIM20":
            return brut_toplam - 20
        elif self.kupon_kodu == "EFSANECUMA":
            return brut_toplam * 0.50
        return brut_toplam

class TopluAlimIndirimi(Indirim):
    def hesapla(self, brut_toplam: float, urun_sayisi: int) -> float:
        if urun_sayisi >= 3:
            return brut_toplam - 30
        return brut_toplam

class IndirimFabrikasi:
    @staticmethod
    def indirim_yarat(indirim_turu: str, kupon_kodu: str = "") -> Indirim:
        tur = indirim_turu.upper()
        if tur == "YUZDE":
            return YuzdeIndirimi()
        elif tur == "KUPON":
            return KuponIndirimi(kupon_kodu)
        elif tur == "TOPLU":
            return TopluAlimIndirimi()
        else:
            raise ValueError(f"Geçersiz indirim türü: {indirim_turu}")

class AlisverisSepeti:
    def __init__(self):
        self._urunler = []

    def urun_ekle(self, urun: Urun):
        self._urunler.append(urun)

    def toplam_hesapla(self, indirim_turu: str, kupon_kodu: str = "") -> float:
        brut_toplam = sum(urun.fiyat for urun in self._urunler)
        urun_sayisi = len(self._urunler)
        
        indirim_stratejisi = IndirimFabrikasi.indirim_yarat(indirim_turu, kupon_kodu)
        
        net_toplam = indirim_stratejisi.hesapla(brut_toplam, urun_sayisi)
        
        return max(0.0, net_toplam)