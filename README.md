D) E-TİCARET SEPETİ

E-ticaret sistemlerinde indirim ve kampanya kuralları iş süreçlerine göre sürekli olarak değişmektedir. Mevcut başlangıç kodundaki if-elif yapısı Open/Closed Prensibini (OCP) doğrudan ihlal ettiği, kodu kırılganlaştırdığı ve bakımı zorlaştırdığı için bu senaryoyu seçtim.





Proje Çalıştırma ve Detaylar



Projenin Amacı ve Ne Yaptığı

Bu proje, başlangıçta monolitik ve "God Class" yapısında olan bir e-ticaret alışveriş sepetinin, 3 faz boyunca nesne yönelimli programlama (OOP) prensipleri ve tasarım örüntüleri (Design Patterns) kullanılarak tamamen esnek, modüler ve genişletilebilir bir mimariye evrilmesini gösterir.



Kullanılan Örüntülerin Özeti

1\. Factory Method (Creational): İndirim nesnelerinin yaratım süreçlerini soyutladı.

2\. Decorator (Structural): Hediye paketi ve hızlı kargo gibi ek özellikleri dinamik olarak sarmaladı.

3\. Adapter (Structural): Sisteme yabancı dış kargo API entegrasyonunu sağladı.

4\. Strategy (Behavioral): Hesaplama algoritmalarını runtime'da değiştirilebilir kıldı.

5\. Observer (Behavioral): Sepet güncellendiğinde yan sistemlere gevşek bağlı haber uçurdu.



Nasıl Çalıştırılır?

Projenin herhangi bir dış bağımlılığı yoktur. Terminale şu komutu yazarak simülasyonu anında izleyebilirsiniz:

```bash

python src/sepet.py

