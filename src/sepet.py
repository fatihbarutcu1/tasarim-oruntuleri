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
        print(f"[STOK SISTEMI] Sepetteki {len(urunler)} adet urun icin stok bloke islemleri tetiklendi.")


class LojistikSistemi(SepetGozlemcisi):
    def guncelle(self, net_toplam: float, urunler: list):
        print(f"[LOJISTIK SISTEMI] {net_toplam} TL tutarindaki sepet icin sevkiyat ve paketleme hazirliklari basladi.")


class HesaplamaStratejisi(ABC):
    @abstractmethod
    def hesapla(self, brut_toplam: float, urun_sayisi: int) -> float:
        pass


class YuzdeIndirimi(HesaplamaStratejisi):
    YUZDE_INDIRIM_ORANI = 0.10

    def hesapla(self, brut_toplam: float, urun_sayisi: int) -> float:
        return brut_toplam * (1 - self.YUZDE_INDIRIM_ORANI)


class KuponIndirimi(HesaplamaStratejisi):
    KUPON_KURALLARI = {
        "INDIRIM20": ("sabit", 20),
        "EFSANECUMA": ("oran", 0.50),
    }

    def __init__(self, kupon_kodu: str):
        self.kupon_kodu = kupon_kodu

    def hesapla(self, brut_toplam: float, urun_sayisi: int) -> float:
        kural = self.KUPON_KURALLARI.get(self.kupon_kodu)
        if kural is None:
            return brut_toplam
        tur, deger = kural
        if tur == "sabit":
            return brut_toplam - deger
        if tur == "oran":
            return brut_toplam * deger
        return brut_toplam


class TopluAlimIndirimi(HesaplamaStratejisi):
    MINIMUM_URUN_SAYISI = 3
    SABIT_INDIRIM_TUTARI = 30

    def hesapla(self, brut_toplam: float, urun_sayisi: int) -> float:
        if urun_sayisi >= self.MINIMUM_URUN_SAYISI:
            return brut_toplam - self.SABIT_INDIRIM_TUTARI
        return brut_toplam


class SepetDekoratoru(HesaplamaStratejisi):
    def __init__(self, sarilan_strateji: HesaplamaStratejisi):
        self._sarilan_strateji = sarilan_strateji

    def hesapla(self, brut_toplam: float, urun_sayisi: int) -> float:
        return self._sarilan_strateji.hesapla(brut_toplam, urun_sayisi)


class HediyePaketiDekoratoru(SepetDekoratoru):
    PAKET_UCRETI = 15.0

    def hesapla(self, brut_toplam: float, urun_sayisi: int) -> float:
        return super().hesapla(brut_toplam, urun_sayisi) + self.PAKET_UCRETI


class HariciKargoHesaplayici:
    KARGO_DESI_CARPANI = 12.5

    def sabit_olmayan_maliyet_bul(self, desi_agirlik: float) -> float:
        return desi_agirlik * self.KARGO_DESI_CARPANI


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
        if tur == "KUPON":
            return KuponIndirimi(kupon_kodu)
        if tur == "TOPLU":
            return TopluAlimIndirimi()
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
    sepet.urun_ekle(Urun("Kablosuz Mouse", 250.0))

    print("--- DURUM 1: Yuzde Indirimi Stratejisi (Fabrika ile) ---")
    sepet.strateji_sec(IndirimFabrikasi.indirim_yarat("YUZDE"))
    print(f"Net Tutar: {sepet.toplam_hesapla()} TL\n")

    print("--- DURUM 2: Toplu Alim Indirimi (Fabrika ile) ---")
    sepet.strateji_sec(IndirimFabrikasi.indirim_yarat("TOPLU"))
    print(f"Net Tutar: {sepet.toplam_hesapla()} TL\n")

    print("--- DURUM 3: Kupon Indirimi + Hediye Paketi (Decorator) ---")
    kupon_ve_paket = HediyePaketiDekoratoru(KuponIndirimi("EFSANECUMA"))
    sepet.strateji_sec(kupon_ve_paket)
    print(f"Net Tutar: {sepet.toplam_hesapla()} TL\n")

    print("--- DURUM 4: Harici Kargo Servisi (Adapter) ---")
    kargo_servisi = HariciKargoHesaplayici()
    kargo_adaptoru = KargoAdaptoru(kargo_servisi, desi=2.0)
    sepet.strateji_sec(kargo_adaptoru)
    print(f"Net Tutar: {sepet.toplam_hesapla()} TL\n")