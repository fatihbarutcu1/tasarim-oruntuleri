Creational (Nesne Yaratma) Örüntüleri

1. Factory Method (Fabrika Metodu)
Uygulandığı Yer:`src/sepet.py` içerisindeki `IndirimFabrikasi` sınıfı ve `indirim_yarat` metodu.
Neden Seçildi? Başlangıç kodunda (Faz 0) kullanıcı sepetine uygulanacak indirim nesnesi doğrudan string kontrollü `if-elif` blokları ile çalışma anında sepetin içinde üretiliyordu. Sisteme yeni bir indirim türü (örneğin "Sadakat Kart İndirimi") eklendiğinde sepet kodunun değiştirilmesi gerekiyordu. Nesne yaratma sorumluluğunu sepetten tamamen ayırıp fabrikaya devretmek için bu örüntü seçilmiştir.
Ne Kazandırdı?Gelişime Açıklık (OCP): Artık yeni bir indirim türü eklemek istediğimizde tek yapmamız gereken `Indirim` sınıfından türeyen yeni bir somut sınıf yazmak ve bunu fabrikaya kaydetmektir. `AlisverisSepeti` sınıfına asla dokunmayız.
Sorumlulukların Ayrılması (SRP): Sepet sınıfı artık sadece ürün ekleme ve genel toplamı yazdırma işine odaklanırken, indirim nesnesi yaratma işi fabrikaya, hesaplama mantıkları ise kendi sınıflarına dağıtıldı.


UML Sınıf Diyagramları (Önce / Sonra)

Önce
```mermaid
classDiagram
    class AlisverisSepeti {
        -list _urunler
        +urun_ekle(urun)
        +toplam_hesapla(indirim_turu, kupon_kodu)
    }
    class Urun {
        +str ad
        +float fiyat
    }
    AlisverisSepeti --> Urun : İçerir

Sonra

classDiagram
    class AlisverisSepeti {
        -list _urunler
        +urun_ekle(urun)
        +toplam_hesapla(indirim_turu, kupon_kodu)
    }
    class IndirimFabrikasi {
        +indirim_yarat(indirim_turu, kupon_kodu)* Indirim
    }
    class Indirim {
        <<abstract>>
        +hesapla(brut_toplam, urun_sayisi)* float
    }
    class YuzdeIndirimi {
        +hesapla(brut_toplam, urun_sayisi) float
    }
    class KuponIndirimi {
        +str kupon_kodu
        +hesapla(brut_toplam, urun_sayisi) float
    }
    class TopluAlimIndirimi {
        +hesapla(brut_toplam, urun_sayisi) float
    }

    Indirim <|-- YuzdeIndirimi : Türetir
    Indirim <|-- KuponIndirimi : Türetir
    Indirim <|-- TopluAlimIndirimi : Türetir
    AlisverisSepeti ..> IndirimFabrikasi : Kullanır
    IndirimFabrikasi ..> Indirim : Üretir

Structural (Yapısal) Örüntüleri

 1. Decorator Pattern 
Nerede Uygulandı: `src/sepet.py` altındaki `SepetDekoratoru`, `HediyePaketiDekoratoru` ve `HizliKargoDekoratoru` sınıflarında.
Neden Seçildi: Müşterilerin sepete eklemek isteyeceği ekstra hizmetler (hediye paketi, ekspres kargo vb.) sepetin ana indirim algoritmasını bozmamalıdır. Kalıtım yerine kompozisyon kullanarak nesne davranışını esnetmek için seçilmiştir.
*Ne Kazandırdı: Mevcut indirim kodlarına dokunmadan, çalışma anında dinamik olarak üst üste eklenebilen esnek ek maliyet yapıları kazandırdı.

2. Adapter Pattern 
Nerede Uygulandı:`src/sepet.py` altındaki `KargoAdaptoru` sınıfında.
Neden Seçildi:Sisteme entegre edilen üçüncü parti `HariciKargoHesaplayici` servisi bizim sistemimizin beklediği `hesapla()` metoduna sahip değildi. Dış kodu değiştiremeyeceğimiz için arayüz uyumsuzluğunu gidermek adına seçilmiştir.
Ne Kazandırdı: Eski veya dış kaynaklı kodların, ana sistem mimarimizi bozmadan sanki bizim bir indirim/maliyet modülümüzmüş gibi esnekçe çalışmasını sağladı.



Mimari Diyagram Güncellemesi 

```mermaid
classDiagram
    class AlisverisSepeti {
        -list _urunler
        +urun_ekle(urun)
        +nihai_tutari_hesapla(hesaplama_stratejisi) float
    }
    class Indirim {
        <<abstract>>
        +hesapla(brut_toplam, urun_sayisi)* float
    }
    class SepetDekoratoru {
        -Indirim _sarilan_indirim
        +hesapla(brut_toplam, urun_sayisi) float
    }
    class HediyePaketiDekoratoru {
        +hesapla(brut_toplam, urun_sayisi) float
    }
    class KargoAdaptoru {
        -HariciKargoHesaplayici _harici_servis
        -float _desi
        +hesapla(brut_toplam, urun_sayisi) float
    }

    Indirim <|-- SepetDekoratoru : Türetir
    SepetDekoratoru <|-- HediyePaketiDekoratoru : Türetir
    Indirim <|-- KargoAdaptoru : Türetir
    AlisverisSepeti ..> Indirim : Kullanır


Faz 3: Behavioral (Davranışsal) Örüntüleri

1. Strategy Pattern (Strateji)
-Nerede Uygulandı: `src/sepet.py` içerisindeki `HesaplamaStratejisi` tabanı ve `AlisverisSepeti.strateji_sec()` metodu.
-Neden Seçildi: İndirim hesaplama algoritmalarının çalışma anında (runtime) dinamik olarak değiştirilebilmesi ve sepetin bu algoritmalardan tamamen bağımsızlaşması için seçildi.
- Ne Kazandırdı: OCP'ye tam uyum sağlandı. Yeni bir indirim algoritması eklemek için sepet sınıfının bir satır kodunu bile değiştirmeye gerek kalmadı.

2. Observer Pattern 
-Nerede Uygulandı: `src/sepet.py` içerisindeki `SepetGozlemcisi` arayüzü ile `StokSistemi` ve `LojistikSistemi` sınıflarında.
- Neden Seçildi: Alışveriş sepetindeki maliyet/durum güncellemelerini, sepet sınıfını diğer sistemlerine bağımlı kılmadan (loose coupling) dış sistemlere bildirmek için seçildi.
- Ne Kazandırdı: Sepet sınıfı artık Stok veya Lojistik sınıflarının adını bile bilmeden onları dolaylı olarak tetikleyebiliyor.