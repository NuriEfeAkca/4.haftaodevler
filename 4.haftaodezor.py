from abc import ABC, abstractmethod
import heapq
import matplotlib.pyplot as plt
import networkx as nx

# Soyut rota stratejisi sınıfı
class RotaStratejisi(ABC):
    @abstractmethod
    def rota_bul(self, harita, baslangic, hedef):
        pass

# Dijkstra algoritması
class Dijkstra(RotaStratejisi):
    def rota_bul(self, harita, baslangic, hedef):
        mesafeler = {sehir: float('inf') for sehir in harita.konumlar}
        mesafeler[baslangic] = 0
        onceki = {}
        pq = [(0, baslangic)]
        
        while pq:
            mevcut_maliyet, mevcut_konum = heapq.heappop(pq)
            
            if mevcut_konum == hedef:
                break
            
            for komsu, maliyet in harita.baglanti[mevcut_konum].items():
                yeni_maliyet = mevcut_maliyet + maliyet
                if yeni_maliyet < mesafeler[komsu]:
                    mesafeler[komsu] = yeni_maliyet
                    onceki[komsu] = mevcut_konum
                    heapq.heappush(pq, (yeni_maliyet, komsu))
        
        yol, nokta = [], hedef
        while nokta in onceki:
            yol.insert(0, nokta)
            nokta = onceki[nokta]
        if yol:
            yol.insert(0, baslangic)
        return yol, mesafeler[hedef]

# BFS algoritması
class BFS(RotaStratejisi):
    def rota_bul(self, harita, baslangic, hedef):
        from collections import deque
        kuyruk = deque([(baslangic, [baslangic])])
        
        while kuyruk:
            mevcut_konum, yol = kuyruk.popleft()
            if mevcut_konum == hedef:
                return yol, len(yol) - 1
            for komsu in harita.baglanti[mevcut_konum]:
                if komsu not in yol:
                    kuyruk.append((komsu, yol + [komsu]))
        return [], float('inf')

# Konum sınıfı
class Konum:
    def __init__(self, isim, x, y):
        self.isim = isim
        self.x = x
        self.y = y

# Harita sınıfı
class Harita:
    def __init__(self):
        self.konumlar = {}
        self.baglanti = {}
        self.strateji = None
    
    def konum_ekle(self, konum):
        self.konumlar[konum.isim] = konum
        self.baglanti[konum.isim] = {}
    
    def baglanti_ekle(self, baslangic, hedef, maliyet):
        self.baglanti[baslangic][hedef] = maliyet
        self.baglanti[hedef][baslangic] = maliyet  # Çift yönlü bağlantı
    
    def set_strateji(self, strateji):
        self.strateji = strateji
    
    def rota_bul(self, baslangic, hedef):
        if self.strateji:
            return self.strateji.rota_bul(self, baslangic, hedef)
        return [], float('inf')
    
    def visualize(self):
        G = nx.Graph()
        for sehir, konum in self.konumlar.items():
            G.add_node(sehir, pos=(konum.x, konum.y))
        for baslangic, hedefler in self.baglanti.items():
            for hedef, maliyet in hedefler.items():
                G.add_edge(baslangic, hedef, weight=maliyet)
        
        pos = nx.get_node_attributes(G, 'pos')
        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, node_color='red', edge_color='gray', style='dashed', node_size=500)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.title("Şehirler Arası Rota Haritası")
        plt.show()

# Örnek kullanım
if __name__ == "__main__":
    harita = Harita()
    harita.konum_ekle(Konum("Istanbul", x=-20, y=60))
    harita.konum_ekle(Konum("Ankara", x=50, y=50))
    harita.konum_ekle(Konum("Izmir", x=-30, y=-30))
    harita.konum_ekle(Konum("Antalya", x=20, y=-40))
    harita.konum_ekle(Konum("Bursa", x=10, y=20))
    harita.konum_ekle(Konum("Konya", x=30, y=0))
    harita.konum_ekle(Konum("Adana", x=80, y=-20))
    harita.konum_ekle(Konum("Trabzon", x=100, y=70))
    
    harita.baglanti_ekle("Istanbul", "Ankara", 450)
    harita.baglanti_ekle("Istanbul", "Bursa", 150)
    harita.baglanti_ekle("Istanbul", "Izmir", 480)
    harita.baglanti_ekle("Ankara", "Konya", 260)
    harita.baglanti_ekle("Ankara", "Trabzon", 780)
    harita.baglanti_ekle("Izmir", "Antalya", 420)
    harita.baglanti_ekle("Antalya", "Konya", 320)
    harita.baglanti_ekle("Konya", "Adana", 340)
    harita.baglanti_ekle("Bursa", "Ankara", 380)
    harita.baglanti_ekle("Bursa", "Izmir", 330)
    harita.baglanti_ekle("Adana", "Trabzon", 890)
    
    harita.set_strateji(Dijkstra())
    yol, maliyet = harita.rota_bul("Istanbul", "Trabzon")
    print(f"Dijkstra ile en kısa yol: {yol}, Toplam maliyet: {maliyet}")
    
    harita.set_strateji(BFS())
    yol, aktarma = harita.rota_bul("Istanbul", "Trabzon")
    print(f"BFS ile en az aktarmalı yol: {yol}, Aktarma sayısı: {aktarma}")
    
    harita.visualize()

