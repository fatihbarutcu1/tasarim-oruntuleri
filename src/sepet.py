class Urun:
    def __init__(self, ad: str, fiyat: float):
        self.ad = ad
        self.fiyat = fiyat

class AlisverisSepeti:
    def __init__(self):
        self._urunler = []

    def urun_ekle(self, urun: Urun):
        self._urunler.append(urun)

    
    def toplam_hesapla(self, indirim_turu: str, kupon_kodu: str = "") -> float:
        toplam = sum(urun.fiyat for urun in self._urunler)

       
        if indirim_turu == "YUZDE":
            toplam = toplam * 0.90
            
        elif indirim_turu == "KUPON":
            if kupon_kodu == "INDIRIM20":
                toplam = toplam - 20
            elif kupon_kodu == "EFSANECUMA":
                toplam = toplam * 0.50  
                
        elif indirim_turu == "TOPLU":
            if len(self._urunler) >= 3:
                toplam = total - 30  

        return max(0.0, toplam)