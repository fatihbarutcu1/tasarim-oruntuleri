# D) E-TİCARET REFAKTÖR VE TASARIM ÖRÜNTÜLERİ PROJESİ

E-ticaret sistemlerinde indirim, kampanya ve lojistik kuralları iş süreçlerine göre sürekli olarak değişkenlik gösterir. Projenin başlangıç (Faz 0) aşamasındaki monolitik ve yoğun `if-elif` blokları barındıran yapısı, Açık/Kapalı Prensibini (OCP) doğrudan ihlal etmekte, kodu son derece kırılganlaştırmakta ve bakımı imkansız hale getirmekteydi. Bu senaryo, söz konusu mimari problemleri tasarım örüntüleri (Design Patterns) yardımıyla çözmek amacıyla seçilmiştir.

---

## 🏗️ Mimari Diyagram (Sınıf Yapısı)

Aşağıdaki sınıf diyagramı, projenin 3 faz sonunda ulaştığı nesne yönelimli yapıyı ve örüntülerin birbiriyle olan bağlarını göstermektedir:

```mermaid
classDiagram
    class AlisverisSepeti {
        -list _urunler
        -list _gozlemciler
        -HesaplamaStratejisi _strateji
        +gozlemci_ekle(gozlemci)
        +gozlemci_cikar(gozlemci)
        +gozlemcilere_haber_ver(net_toplam)
        +strateji_sec(yeni_strateji)
        +urun_ekle(urun)
        +toplam_hesapla() float
    }

    class HesaplamaStratejisi {
        <<interface>>
        +hesapla(brut_toplam, urun_sayisi) float
    }

    class SepetGozlemcisi {
        <<interface>>
        +guncelle(net_toplam, urunler)
    }

    HesaplamaStratejisi <|-- YuzdeIndirimi
    HesaplamaStratejisi <|-- KuponIndirimi
    HesaplamaStratejisi <|-- TopluAlimIndirimi
    HesaplamaStratejisi <|-- SepetDekoratoru
    HesaplamaStratejisi <|-- KargoAdaptoru

    SepetDekoratoru <|-- HediyePaketiDekoratoru
    AlisverisSepeti --> HesaplamaStratejisi : Kullanır (Strategy)
    AlisverisSepeti --> SepetGozlemcisi : Bildirir (Observer)

    SepetGozlemcisi <|-- StokSistemi
    SepetGozlemcisi <|-- LojistikSistemi
🛠️ Proje Çalıştırma ve Detaylar
Projenin Amacı ve Ne Yaptığı
Bu projenin temel amacı; başlangıçta tek bir sınıf içerisine sıkışmış olan, SOLID prensiplerine aykırı ve genişletilmesi imkansız olan bir e-ticaret sepet hesaplama motorunu, endüstriyel standartlara uygun kurumsal bir mimariye dönüştürmektir.

Sistem, sepete eklenen ürünlerin brüt tutarlarını hesaplar. Ardından, runtime (çalışma anında) seçilen Strategy örüntüsüne göre indirimleri (Kupon, Yüzde veya Toplu Alım) uygular. Eğer yapıya ek operasyonel maliyetler (Hediye paketi, harici kargo entegrasyonu vb.) dahil edilirse, Decorator ve Adapter yapıları devreye girerek bu fiyatları dinamik olarak sepet tutarına yansıtır. Hesaplama bittiği an Observer yapısı sayesinde eldeki nihai veri Stok ve Lojistik gibi harici alt sistemlere asenkron/gevşek bağlı bir şekilde raporlanır.

Kullanılan Örüntülerin Özeti
Factory Method (Creational): İndirim nesnelerinin yaratım süreçlerini soyutlayarak sepet sınıfını somut indirim sınıflarına bağımlı olmaktan kurtardı.

Decorator (Structural): Hediye paketi gibi ek finansal/operasyonel özellikleri, mevcut indirim yapılarını bozmadan dinamik olarak sarmalamayı sağladı.

Adapter (Structural): Sisteme tamamen yabancı olan harici kargo hesaplama API entegrasyonunun sisteme uyum sağlamasını mümkün kıldı.

Strategy (Behavioral): Hesaplama ve indirim algoritmalarını runtime'da (çalışma anında) dinamik olarak değiştirilebilir ve seçilebilir kıldı.

Observer (Behavioral): Sepet güncellendiğinde veya nihai tutar netleştiğinde yan sistemlerin (Stok ve Lojistik) gevşek bağlı (loose coupling) bir şekilde haberdar edilmesini sağladı.

Nasıl Çalıştırılır?
Projenin herhangi bir üçüncü parti kütüphane bağımlılığı yoktur. Sadece yerel Python ortamının kurulu olması yeterlidir. Terminali veya Git Bash ekranını açıp projenin kök dizinine gelerek şu komutu yazıp simülasyon çıktılarını anında izleyebilirsiniz:

Bash
python src/sepet.py