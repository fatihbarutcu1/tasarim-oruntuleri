from abc import ABC, abstractmethod

class Urun:
    def __init__(self, ad: str, fiyat: float):
        self.ad = ad
        self.fiyat = fiyat
class SepetGozlemcisi(ABC):
    @abstractmethod
    def guncelle(self, net_tulam: float, urunler: list):
        pass

class StokSistemi(SepetGozlemcisi):
    def guncelle(self, net_tulam: float, urunler: list):
        print(f"[STOK SİSTEMİ] Sepetteki {len(urunler)} adet ürün için stok bloke işlemleri tetiklendi.")

class LojistikSistemi(SepetGozlemcisi):
    def guncelle(self, net_tulam: float, urunler: list):
        if net_tulam > 500:
            print(f"[LOJİSTİK SİSTEMİ] Yüksek tutarlı sipariş ({net_tulam} TL). Özel paketleme sırasına alındı.")


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

class AlisverisSepeti:
    def __init__(self):
        self._urunler = []
        self._gozlemciler = [] # Observer listesi
        self._strateji = YuzdeIndirimi() # Varsayılan Strategy

        def gozlemci_ekle(self, gozlemci: SepetGozlemcisi):
        if gozlemci not in self._gozlemciler:
            self._gozlemciler.append(gozlemci)

    def gozlemci_cikar(self, gozlemci: SepetGozlemcisi):
        self._gozlemciler.remove(gozlemci)

    def gozlemcilere_haber_ver(self, net_toplam: float):
        for gozlemci in self._gozlemciler:
            gozlemci.guncelle(net_toplam, self._urunler)

    
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
    
    sepet.urun_ekle(Urun("Oyuncu Kulaklığı", 450.0))
    sepet.urun_ekle(Urun("Mousepad", 100.0))
    
    print("--- 1. Durum: Varsayılan Yüzde İndirimi Stratejisi ---")
    sepet.toplam_hesapla()
    
    print("\n--- 2. Durum: Stratejiyi Kupon İndirimi + Hediye Paketi (Decorator) Olarak Değiştirme ---")
    kupon_ve_paket = HediyePaketiDekoratoru(KuponIndirimi("EFSANECUMA"))
    sepet.strateji_sec(kupon_ve_paket)
    sepet.toplam_hesapla()