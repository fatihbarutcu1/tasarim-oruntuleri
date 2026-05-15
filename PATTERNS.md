# Projede Kullanılan Tasarım Örüntüleri (PATTERNS.md)

## 🏗️ Faz 1: Creational (Nesne Yaratma) Örüntüleri

### 1. Factory Method (Fabrika Metodu)
- **Uygulandığı Yer:** `src/sepet.py` içerisindeki `IndirimFabrikasi` sınıfı ve `indirim_yarat` metodu.
- **Neden Seçildi?** Başlangıç kodunda (Faz 0) kullanıcı sepetine uygulanacak indirim nesnesi doğrudan string kontrollü `if-elif` blokları ile çalışma anında sepetin içinde üretiliyordu. Sisteme yeni bir indirim türü (örneğin "Sadakat Kart İndirimi") eklendiğinde sepet kodunun değiştirilmesi gerekiyordu. Nesne yaratma sorumluluğunu sepetten tamamen ayırıp fabrikaya devretmek için bu örüntü seçilmiştir.
- **Ne Kazandırdı?** - **Gelişime Açıklık (OCP):** Artık yeni bir indirim türü eklemek istediğimizde tek yapmamız gereken `Indirim` sınıfından türeyen yeni bir somut sınıf yazmak ve bunu fabrikaya kaydetmektir. `AlisverisSepeti` sınıfına asla dokunmayız.
  - **Sorumlulukların Ayrılması (SRP):** Sepet sınıfı artık sadece ürün ekleme ve genel toplamı yazdırma işine odaklanırken, indirim nesnesi yaratma işi fabrikaya, hesaplama mantıkları ise kendi sınıflarına dağıtıldı.

---

### 📊 UML Sınıf Diyagramları (Önce / Sonra)

#### ❌ Önce (Faz 0 - Spaghetti Yapı)
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