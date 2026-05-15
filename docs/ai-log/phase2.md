Yapay Zeka Log (Structural Örüntüler)

AI ile Örüntü Tartışması (Prompt)
"E-ticaret sepet projemizde sisteme harici bir kargo firmasının API'sini entegre etmek istiyoruz. Bu yapısal entegrasyon için Adapter pattern mı daha uygundur, yoksa Facade pattern mı? İki örüntünün farkını bizim senaryomuz üzerinden açıklayıp bir kritik yapar mısın?"

AI Ne Yanıtladı?
AI, her iki örüntünün de yapısal (Structural) olduğunu ancak amaçlarının tamamen farklı olduğunu belirtti:
Adapter: Mevcut bir arayüzü (Interface), sistemin beklediği başka bir arayüzle uyumlu hale getirmek (çevirmek) için kullanılır.
Facade:Karmaşık ve çok sayıda sınıftan oluşan bir alt sistemi (Subsystem), tek bir basitleştirilmiş sınıf arkasına gizleyerek kullanımı kolaylaştırmak için kullanılır.
Bizim durumumuzda dışarıdan gelen `HariciKargoHesaplayici` sınıfının imzasını, kendi sistemimizdeki `Indirim` arayüzüne uydurmamız gerektiği için AI bize Adapter örüntüsünün kesinlikle doğru tercih olduğunu söyledi.

AI'ın Eksik/Yanlış Önerdiği Nokta ve Benim Müdahalem 
AI, Decorator Pattern uygulamasını önerirken çok büyük bir tasarım hatası yaptı. Bana verdiği ilk kod taslağında `SepetDekoratoru` sınıfını doğrudan `AlisverisSepeti` sınıfından türetmeye çalıştı.. 

Neden Yanlıştı? Decorator örüntüsünün temel amacı, sınıfları kalıtımla şişirmek yerine kompozisyon kullanarak nesnelere dinamik sorumluluklar yüklemektir. Eğer sepeti doğrudan kalıtımla süslemeye kalkarsak, çalışma anında birden fazla dekoratörü  esnek bir şekilde üst üste sarmalayamayız . 

Benim Çözümüm:Tasarımı düzelterek `SepetDekoratoru` sınıfını, sepetin hesaplama motorunun bağlı olduğu soyut `Indirim` taban sınıfından türettim ve içerisine bir `Indirim` nesnesi sarmaladım . Böylece `HediyePaketiDekoratoru(HizliKargoDekoratoru(YuzdeIndirimi()))` şeklinde zincirleme ve esnek sarmalamayı Python'da güvenle yapabilmiş olduk.