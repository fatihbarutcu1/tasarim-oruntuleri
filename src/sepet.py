from abc import ABC, abstractmethod

class Urun:
    def __init__(self, ad: str, fiyat: float):
        self.ad = ad
        self.fiyat = fiyat

class SepetGozlemcisi(ABC):
    @abstractmethod
    def guncelle(self, net_toplam: float, urunler: list):
        pass

class StokSistemi(SepetGozlemcisi):
    def guncelle(self, net_toplam: float, urunler: list):
        print(f"[STOK SİSTEMİ] Sepetteki {len(urunler)} adet ürün için stok bloke işlemleri tetiklendi.")

class LojistikSistemi(SepetGozlemcisi):
    def guncelle(self, net_toplam: float, urunler: list):
        print(f"[LOJİSTİK SİSTEMİ] {net_toplam} TL tutarındaki sepet için sevkiyat ve paketleme hazırlıkları başladı.")

class HesaplamaStratejisi(ABC):
    @abstractmethod
    def hesapla(self, brut_toplam: float, urun_sayisi: int) -> float:
        pass

class YuzdeIndirimi(HesaplamaStratejisi):
    def hesapla(self, brut_toplam: float, urun_sayisi: int) -> float:
        return brut_toplam * 0.90

class KuponIndirimi(HesaplamaStratejisi):
    def __init__(self, kupon_kodu: str):
        self.kupon_kodu = kupon_kodu

    def hesapla(self, brut_toplam: float, urun_sayisi: int) -> float:
        if self.kupon_kodu == "INDIRIM20":
            return brut_toplam - 20
        elif self.kupon_kodu == "EFSANECUMA":
            return brut_toplam * 0.50
        return brut_toplam

class TopluAlimIndirimi(HesaplamaStratejisi):
    def hesapla(self, brut_toplam: float, urun_sayisi: int) -> float:
        if urun_sayisi >= 3:
            return brut_toplam - 30
        return brut_toplam

class SepetDekoratoru(HesaplamaStratejisi):
    def __init__(self, sarilan_strateji: HesaplamaStratejisi):
        self._sarilan_strateji = sarilan_strateji

    def hesapla(self, brut_toplam: float, urun_sayisi: int) -> float:
        return self._sarilan_strateji.hesapla(brut_toplam, urun_sayisi)

class HediyePaketiDekoratoru(SepetDekoratoru):
    def __init__(self, sarilan_strateji: HesaplamaStratejisi):
        super().__init__(sarilan_strateji)

    def hesapla(self, brut_toplam: float, urun_sayisi: int) -> float:
        return super().hesapla(brut_toplam, urun_sayisi) + 15.0

class HariciKargoHesaplayici:
    def sabit_olmayan_maliyet_bul(self, desi_agirlik: float) -> float:
        return desi_agirlik * 12.5

class KargoAdaptoru(HesaplamaStratejisi):
    def __init__(self, harici_servis: HariciKargoHesaplayici, desi: float):
        self._harici_servis = harici_servis
        self._desi = desi

    def hesapla(self, brut_toplam: float, urun_sayisi: int) -> float:
        return brut_toplam + self._harici_servis.sabit_olmayan_maliyet_bul(self._desi)

class IndirimFabrikasi:
    @staticmethod
    def indirim_yarat(indirim_turu: str, kupon_kodu: str = "") -> HesaplamaStratejisi:
        tur = indirim_turu.upper()
        if tur == "YUZDE":
            return YuzdeIndirimi()
        elif tur == "KUPON":
            return KuponIndirimi(kupon_kodu)
        elif tur == "TOPLU":
            return TopluAlimIndirimi()
        else:
            raise ValueError(f"Gecersiz indirim turu: {indirim_turu}")

class AlisverisSepeti:
    def __init__(self):
        self._urunler = []
        self._gozlemciler = []
        self._strateji = YuzdeIndirimi()

    def gozlemci_ekle(self, gozlemci: SepetGozlemcisi):
        if gozlemci not in self._gozlemciler:
            self._gozlemciler.append(gozlemci)

    def gozlemci_cikar(self, gozlemci: SepetGozlemcisi):
        if gozlemci in self._gozlemciler:
            self._gozlemciler.remove(gozlemci)

    def gozlemcilere_haber_ver(self, net_toplam: float):
        for gozlemci in self._gozlemciler:
            gozlemci.guncelle(net_toplam, self._urunler)

    def Crane(self, yeni_strateji: HesaplamaStratejisi):
        self._strateji = yeni_strateji

    def strateji_sec(self, yeni_strateji: HesaplamaStratejisi):
        self._strateji = yeni_strateji

    def urun_ekle(self, urun: Urun):
        self._urunler.append(urun)

    def toplam_hesapla(self) -> float:
        brut_toplam = sum(urun.fiyat for urun in self._urunler)
        urun_sayisi = len(self._urunler)
        net_toplam = self._strateji.hesapla(brut_toplam, urun_sayisi)
        net_toplam = max(0.0, net_toplam)
        self.gozlemcilere_haber_ver(net_toplam)
        return net_toplam

if __name__ == "__main__":
    sepet = AlisverisSepeti()
    sepet.gozlemci_ekle(StokSistemi())
    sepet.gozlemci_ekle(LojistikSistemi())
    sepet.urun_ekle(Urun("Oyuncu Kulakligi", 450.0))
    sepet.urun_ekle(Urun("Mousepad", 100.0))
    print("--- DURUM 1: Yuzde Indirimi Stratejisi ---")
    sepet.toplam_hesapla()
    print("\n--- DURUM 2: Kupon + Hediye Paketi Dekoratoru ---")
    kupon_ve_paket = HediyePaketiDekoratoru(KuponIndirimi("EFSANECUMA"))
    sepet.strateji_sec(kupon_ve_paket)
    sepet.toplam_hesapla()