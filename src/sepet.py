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

class SepetDekoratoru(Indirim):
    def __init__(self, sarilan_indirim: Indirim):
        self._sarilan_indirim = sarilan_indirim

    def hesapla(self, brut_toplam: float, urun_sayisi: int) -> float:
        return self._sarilan_indirim.hesapla(brut_toplam, urun_sayisi)

class HediyePaketiDekoratoru(SepetDekoratoru):
    def hesapla(self, brut_toplam: float, urun_sayisi: int) -> float:
        mevcut_tutar = super().hesapla(brut_toplam, urun_sayisi)
        return mevcut_tutar + 15.0

class HizliKargoDekoratoru(SepetDekoratoru):
    def hesapla(self, brut_toplam: float, urun_sayisi: int) -> float:
        mevcut_tutar = super().hesapla(brut_toplam, urun_sayisi)
        return mevcut_tutar + 50.0


class HariciKargoHesaplayici:
    def sabit_olmayan_maliyet_bul(self, desi_agirlik: float) -> float:
        return desi_agirlik * 12.5

class KargoAdaptoru(Indirim):
    def __init__(self, harici_servis: HariciKargoHesaplayici, desi: float):
        self._harici_servis = harici_servis
        self._desi = desi

    def hesapla(self, brut_toplam: float, urun_sayisi: int) -> float:        
        return brut_toplam + self._harici_servis.sabit_olmayan_maliyet_bul(self._desi)

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

    def nihai_tutari_hesapla(self, hesaplama_stratejisi: Indirim) -> float:
        brut_toplam = sum(urun.fiyat for urun in self._urunler)
        urun_sayisi = len(self._urunler)
        
        net_toplam = hesaplama_stratejisi.hesapla(brut_toplam, urun_sayisi)
        return max(0.0, net_toplam)