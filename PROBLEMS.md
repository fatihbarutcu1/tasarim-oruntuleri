# PROBLEMS.md

> **Faz 0 - Baslangic Kodunun Analizi**
>
> Refactor oncesi baslangic kodu `src/_legacy/sepet_v0.py` dosyasinda referans olarak saklanmaktadir. Bu belge, o kodda tespit edilen tasarim sorunlarini ve Yapay Zeka destekli ikinci bir analizle karsilastirmasini icerir.

---

## 1. Benim Tespit Ettigim Sorunlar

### Sorun 1 - Open/Closed Principle (OCP) Ihlali
`toplam_hesapla` metodu, yeni bir indirim turu eklendiginde mutlaka degistirilmek zorunda. Bu, bir sinifin "degisime kapali, genislemeye acik" olmasi gerektigini soyleyen OCP'yi dogrudan ihlal ediyor; cunku her yeni kampanya tipi mevcut kodu kirma riskiyle birlikte geliyor.

### Sorun 2 - Single Responsibility Principle (SRP) Ihlali
`AlisverisSepeti` sinifi tek basina hem sepet yonetimi, hem indirim hesaplamasi, hem stok bildirimi, hem de lojistik tetikleme isini yapiyor. Bu kadar sorumlulugu olan bir sinif "God Class" haline gelir; degistirilmesi gereken her ozellik bu tek dosyayi etkiler.

### Sorun 3 - Magic Numbers (Sihirli Sayilar)
Kod icerisinde `0.90`, `0.50`, `20`, `30`, `3` gibi anlamsiz sayilar dogrudan gomulu. Bu sayilarin hangi is kuralini temsil ettigi belli olmadigi icin kod okunmuyor; ayrica ayni sayi birden fazla yerde gectiginde tutarsizlik riski artiyor.

### Sorun 4 - Tip Guvenligi Yok (String ile Tip Kontrolu)
`indirim_turu: str` parametresi yazim hatalarina (`"YUZDE"` yerine `"yuzde"` veya `"YUZDEE"`) tamamen acik. Bir Enum veya nesne hierarjisi olmadigi icin compiler/IDE bu hatayi yakalayamiyor, hata ancak runtime'da ortaya cikiyor.

### Sorun 5 - Gereksiz Coupling: `kupon_kodu` Parametresi
`toplam_hesapla(indirim_turu, kupon_kodu)` imzasi, yuzde indirimi kullanildiginda bile `kupon_kodu` parametresinin geciliyor olmasini gerektiriyor. Sepet sinifi, kullanmadigi parametreleri bilmek zorunda kaliyor ve bu, sinifi gereksizce baska kavramlara baglıyor.

### Sorun 6 - Indirimler Birlestirilemiyor
Mevcut yapida ayni anda hem yuzde indirimi hem kupon indirimi uygulamak imkansiz, cunku if-elif zinciri sadece bir dalda calisiyor. Gercek hayatta "hem indirim haftasi hem kupon" gibi kombine kampanyalar gerekiyor, ama bu kod buna izin vermiyor.

### Sorun 7 - Bildirim Sistemi Sepete Gomulu
Stok ve Lojistik bildirimleri sepetin icinde `print` ile yapiliyor. Yeni bir bildirim sistemi (orn. Mail, SMS) eklenmek istendiginde sepet kodu tekrar acilip degistirilmek zorunda; bu da gevsek baglilik (loose coupling) ilkesini cigniyor.

### Sorun 8 - Gizli Bug: `total` Degiskeni Tanimsiz
TOPLU indirim dalinda `net_toplam = total - 30` yaziyor; ancak `total` adli bir degisken hicbir yerde tanimli degil. Bu, kod hicbir zaman bu kosula girmedigi icin patlamiyor ama girdiginde `NameError` firlatacak; bir test eksikligi gostergesi.

---

## 2. Yapay Zeka Karsi Analizi

### AI'a Sorulan Prompt

> "Bu kodda hangi tasarim sorunlarini goruyorsun? Hangi tasarim oruntuleri bu sorunlari cozebilir? Her sorun icin kisa bir aciklama yaz."

### AI'in Cevabi (Ozet)

1. `toplam_hesapla` cok fazla is yapiyor - **SRP ihlali**. Cozum: **Strategy Pattern**.
2. Surekli if-elif kullanilmis - kod buyudukce yonetimi zorlasiyor. Cozum: **Strategy Pattern**.
3. `"YUZDE"` gibi string kullanimi var - yazim hatasina acik. Cozum: **Enum**.
4. Kupon kurallari metoda gomulmus - yeni kampanya icin kod degistirmek gerekir. Cozum: **Factory Pattern**.
5. Kupon ve indirimler primitive tiplerle tutuluyor - domain yapisi zayif. Cozum: **Value Object**.
6. Hatali indirim turlerinde kontrol yok - sessiz hatalar olabilir. Cozum: **Null Object** veya istisna yonetimi.
7. Kodda `total = total - 30` ifadesinde `total` tanimsiz - bir bug. Cozum: **Birim test yazilmasi**.
8. Indirimler birlikte calisamiyor - sistem esnek degil. Cozum: **Chain of Responsibility Pattern**.

---

## 3. Karsilastirma: AI Ne Gordu, Ben Ne Gordum?

| Konu | Benim Yaklasimim | AI'in Yaklasimi |
|---|---|---|
| Analiz acisi | SOLID prensipleri ve kod kokulari (code smell) | Her soruna dogrudan bir tasarim ortuntusu eslesimi |
| Odak | "Ne yanlis?" sorusuna agirlik | "Nasil cozulur?" sorusuna agirlik |
| Bug tespiti | `total` degiskeni tanimsiz hatasini buldum | AI da bunu buldu ancak coz olarak sadece "test yazin" dedi |
| Eksik gordugum | Enum onerisini ben yapmadim, AI ekledi | - |
| Eksik gordugu | Bildirim sisteminin sepete gomulu olmasi (Sorun 7) | AI bu noktayi atladi |

### Sonuc

AI ile kendi analizim **birbirini tamamladi**. Ben kod kalitesi gozuyle, kod kokularini (magic numbers, gereksiz parametre, God Class) tespit ettim. AI ise her sorunun yanina bir cozum oruntusu kondurarak "nasil cozulur" boyutunu ekledi. Ozellikle "indirimlerin birlestirilebilmesi" icin onerdigi **Chain of Responsibility** veya benim daha sonra tercih ettigim **Decorator** seceneklerini tartismaya acmak proje icin onemli bir donum noktasi oldu.

AI'in kacirdigi en kritik nokta, **bildirim sisteminin sepetin icine gomulmus olmasi (Sorun 7)** idi. Bu, sonraki fazlarda Observer Pattern'a gectigimizde kazanim yarattigi icin ilk gozden gecirmede tespit edilmis olmasi onemliydi.