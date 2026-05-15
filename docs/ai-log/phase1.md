Yapay Zeka Log (Creational Örüntüler)
AI'a Ne Soruldu? (Prompt)
"E-ticaret sepet uygulamasında indirim hesaplama mantıklarının (Yüzde İndirimi, Kupon İndirimi, Toplu Alım İndirimi) sepet sınıfı içinde yaygın if-elif bloklarıyla yapılması Open/Closed Prensibini (OCP) ihlal ediyor. Nesne yaratma ve yönetim sorumluluğunu AlisverisSepeti sınıfından soyutlamak adına Factory Method örüntüsünü Türkçe fonksiyon/sınıf isimleriyle Python dilinde nasıl kurgulayabiliriz? Kod incelemesi (review) ve esnek bir mimari önerisi yapabilir misin?"

AI Ne Yanıtladı? 
AI, mevcut `AlisverisSepeti` sınıfının hem sepet yönetimini yapıp hem de indirim mantıklarını içermesinin Single Responsibility (SRP) ve Open/Closed (OCP) prensiplerine aykırı olduğunu doğruladı. Çözüm olarak:
1. `abc` modülü kullanılarak soyut bir `Indirim` taban sınıfı oluşturulmasını,
2. Her indirim türünün (`YuzdeIndirimi`, `KuponIndirimi`, `TopluAlimIndirimi`) bu sınıftan türetilerek kendi hesaplama mantıklarını kapsüllemesini (encapsulation),
3. Parametrik olarak bu nesneleri üreten merkezi bir `IndirimFabrikasi` (Factory) kurulmasını önerdi.

Ben Ne Uyguladım ve Neden?
AI'ın sunduğu nesne yönelimli mimari önerisini tamamen benimsedim ve kodu kendi ellerimle yazarak uyguladım. 
Aynılıklar:Soyut taban sınıf mantığı (`Indirim`) ve somut indirim stratejilerinin ayrıştırılması mimarisini birebir uyguladım. Böylece sepet sınıfının katı bağlılığı (tight coupling) giderildi.
Farklılıklar/Detaylar: AI ilk başta Java tarzı çoklu fabrika sınıfları (Creator alt sınıfları) önerdi. Ancak Python'ın dinamik ve pratik yapısına daha uygun, okunabilirliği yüksek olan `@staticmethod` desenli tek bir merkezi `IndirimFabrikasi` sınıfı kurmayı tercih ettim. Bu sayede ödev isterlerini tam karşılarken kodun aşırı karmaşıklaşmasını (over-engineering) engellemiş oldum.
