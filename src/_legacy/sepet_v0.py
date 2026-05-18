

class Urun:
    def __init__(self, ad, fiyat):
        self.ad = ad
        self.fiyat = fiyat


class AlisverisSepeti:
    

    def __init__(self):
        self._urunler = []

    def urun_ekle(self, urun):
        self._urunler.append(urun)

    def toplam_hesapla(self, indirim_turu: str, kupon_kodu: str = ""):
                brut_toplam = 0
        for urun in self._urunler:
            brut_toplam += urun.fiyat

        urun_sayisi = len(self._urunler)
        net_toplam = brut_toplam

        
        if indirim_turu == "YUZDE":
            net_toplam = brut_toplam * 0.90

        elif indirim_turu == "KUPON":
            
            if kupon_kodu == "INDIRIM20":
                
                net_toplam = brut_toplam - 20
            elif kupon_kodu == "EFSANECUMA":
                
                net_toplam = brut_toplam * 0.50
            else:
                net_toplam = brut_toplam

        elif indirim_turu == "TOPLU":
            
            if urun_sayisi >= 3:
                
                net_toplam = brut_toplam - 30

        
        print(f"[STOK SISTEMI] {len(self._urunler)} urun icin stok bloke edildi.")
        print(f"[LOJISTIK] {net_toplam} TL tutarinda sevkiyat hazirligi.")

        
        return net_toplam


if __name__ == "__main__":
    sepet = AlisverisSepeti()
    sepet.urun_ekle(Urun("Oyuncu Kulakligi", 450.0))
    sepet.urun_ekle(Urun("Mousepad", 100.0))

    print("--- YUZDE Indirimi ---")
    print(sepet.toplam_hesapla("YUZDE"))

    print("--- KUPON Indirimi (EFSANECUMA) ---")
    print(sepet.toplam_hesapla("KUPON", "EFSANECUMA"))
