from abc import ABC, abstractmethod

class EnvanterEsyasi(ABC):
    def __init__(self, ad, agirlik, dayaniklilik):
        self.ad = ad
        self.agirlik = agirlik
        self.dayaniklilik = dayaniklilik
    
    @abstractmethod
    def kullan(self):
        pass

class Silah(EnvanterEsyasi):
    def __init__(self, ad, agirlik, dayaniklilik, hasar):
        super().__init__(ad, agirlik, dayaniklilik)
        self.hasar = hasar
    
    def kullan(self):
        if self.dayaniklilik > 0:
            self.dayaniklilik -= 5
            print(f"{self.ad} kullanıldı! Kalan dayanıklılık: {self.dayaniklilik}")
        else:
            print(f"{self.ad} kırıldı ve kullanılamaz!")

class Zirh(EnvanterEsyasi):
    def __init__(self, ad, agirlik, dayaniklilik, koruma):
        super().__init__(ad, agirlik, dayaniklilik)
        self.koruma = koruma
    
    def kullan(self):
        if self.dayaniklilik > 0:
            self.dayaniklilik -= 3
            print(f"{self.ad} kullanıldı! Kalan dayanıklılık: {self.dayaniklilik}")
        else:
            print(f"{self.ad} parçalandı ve koruma sağlamıyor!")

class Oyuncu:
    def __init__(self, isim, max_agirlik):
        self.isim = isim
        self.max_agirlik = max_agirlik
        self.envanter = []
    
    def envanter_agirlik(self):
        return sum(esya.agirlik for esya in self.envanter)
    
    def esya_ekle(self, esya):
        if self.envanter_agirlik() + esya.agirlik <= self.max_agirlik:
            self.envanter.append(esya)
            print(f"{esya.ad} envantere eklendi.")
        else:
            print("Envanter kapasitesi aşıldı!")
    
    def esya_cikar(self, ad):
        for esya in self.envanter:
            if esya.ad == ad:
                self.envanter.remove(esya)
                print(f"{ad} envanterden çıkarıldı.")
                return
        print(f"{ad} envanterde bulunamadı!")
    
    def esya_kullan(self, ad):
        for esya in self.envanter:
            if esya.ad == ad:
                esya.kullan()
                return
        print(f"{ad} envanterde bulunamadı!")
    
    def envanter_goster(self):
        print(f"{self.isim} Envanteri:")
        print(f"Toplam Ağırlık: {self.envanter_agirlik()}/{self.max_agirlik}kg")
        for esya in self.envanter:
            if isinstance(esya, Silah):
                print(f"- Silah: {esya.ad} | Hasar: {esya.hasar} | Ağırlık: {esya.agirlik}kg")
            elif isinstance(esya, Zirh):
                print(f"- Zırh: {esya.ad} | Koruma: {esya.koruma} | Ağırlık: {esya.agirlik}kg")

if __name__ == "__main__":
    oyuncu = Oyuncu("GiantDad", 200.3)
    kilic = Silah("Zweihander", 10.0, 200, 130)
    zirh = Zirh("Dev Zırhı", 50.0, 280, 372.8)
    
    oyuncu.esya_ekle(kilic)
    oyuncu.esya_ekle(zirh)
    oyuncu.envanter_goster()
    
    oyuncu.esya_kullan("Zweihander")
    oyuncu.esya_kullan("Dev Zırhı")
    
    for _ in range(5):
        oyuncu.esya_kullan("Zweihander")
    
    oyuncu.esya_cikar("Dev Zırhı")
    oyuncu.envanter_goster()
