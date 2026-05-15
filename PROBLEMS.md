1- Open/Closed Principle (OCP) — toplam_hesapla metodu kapalı değil, sürekli değiştirilmesi gerekiyor
2- Single Responsibility Principle (SRP)  — AlisverisSepeti sınıfı hem sepet yönetiyor hem indirim hesaplıyor
3- Magic numbers / hardcoded değerler her yerde
0.90, 0.50, 20, 30, 3 gibi sayılar koda gömülmüş. 
4- Type hint olarak str kullanımı — indirim_turu: str tip güvenliği sağlamıyor
5- kupon_kodu parametresi gereksiz coupling yaratıyor
6- İndirimler birleştirilemiyor.

AI ne gördü, siz ne gördünüz, aralarında fark var mı?

AI Cevabı

1-toplam_hesapla çok fazla iş yapıyor → Single Responsibility Principle ihlali.
Çözüm: Strategy Pattern
2-Sürekli if-elif kullanılmış → Kod büyüdükçe yönetmesi zorlaşır.
Çözüm: Strategy Pattern
3-"YUZDE" gibi string kullanımı var → Yazım hatasına açık.
Çözüm: Enum kullanımı
4-Kupon kuralları metoda gömülmüş → Yeni kampanya için kod değiştirmek gerekir.
Çözüm: Factory Pattern
5-Kupon ve indirimler primitive tiplerle tutuluyor → Domain yapısı zayıf.
Çözüm: Value Object
6-Hatalı indirim türlerinde kontrol yok → Sessiz hatalar oluşabilir.
Çözüm: Null Object veya Exception yönetimi

7-Kodda bug var:

toplam = total - 30

total tanımsız.
Çözüm: Unit test yazılması

8-İndirimler birlikte çalışamıyor → Sistem esnek değil.
Çözüm: Chain of Responsibility Pattern

AI ve benim aramdaki farklar

Benim analizim daha çok SOLID prensipleri ve somut kod kokuları (magic numbers, gereksiz parametre) üzerinden ilerlemiş — yani "ne yanlış?" sorusuna odaklanmışım. AI'ın analizi ise her sorunun yanına bir tasarım deseni çözümü (Strategy, Factory, Value Object, Chain of Responsibility) koymuş — yani "nasıl çözülür?" boyutunu da eklemiş.
Ben kod kalitesi gözüyle bakmışım, AI çözüm odaklı bakmış.



