import time
import random
import pandas as pd
import matplotlib.pyplot as plt

class CBF_IHA:
    def __init__(self, isim):
        self.isim = isim
        # 1. FİZİKSEL VE STABİLİTE VERİLERİ (3 Eksen)
        self.irtifa = 0.0
        self.roll = 0.0             
        self.pitch = 0.0            
        self.yaw = 0.0              
        self.titresim = 0.0         
        self.batarya = 100          
        
        # 2. SİSTEM VE HABERLEŞME SAĞLIĞI
        self.gecikme = 10           
        self.islemci_yuku = 20      
        self.sensor_tutarliligi = 100 
        
        # 3. SİBER GÜVENLİK KATMANI
        self.replay_saldirisi = False
        self.veri_enjeksiyonu_riski = 0 
        self.komut_dogrulama = True 
        
        self.ucus_modu = "Normal"
        self.kara_kutu = []         # Blackbox kayıtları [cite: 13]

    def guven_skoru_hesapla(self):
        """Bütünsel değerlendirme yapan CBF algoritması [cite: 87]"""
        skor = 100
        
        # Fiziksel Limitler
        if abs(self.roll) > 30 or abs(self.pitch) > 30: skor -= 15
        if self.titresim > 70: skor -= 10 
        
        # Haberleşme ve Sensör Tutarlılığı [cite: 36, 38]
        if self.sensor_tutarliligi < 95: skor -= 20 
        if self.gecikme > 200: skor -= 15 
        
        # Siber Güvenlik Katmanı
        if self.replay_saldirisi: skor -= 50 
        if self.islemci_yuku > 90: skor -= 30 
        if not self.komut_dogrulama: skor -= 40 
        
        # Donanımsal Kritik Hata [cite: 73]
        if self.batarya < 20: skor -= 40 

        return max(skor, 0)

    def ucus_modu_belirle(self, skor):
        """Güven skoruna göre dinamik davranış kararı [cite: 48]"""
        if skor >= 80:
            self.ucus_modu = "Normal Uçuş" # [cite: 51]
        elif 50 <= skor < 80:
            self.ucus_modu = "Temkinli Mod" # [cite: 49]
        else:
            self.ucus_modu = "Güvenli Mod (FAIL-SAFE)" # [cite: 50, 62]

    def gorev_dongusu(self, sure=30):
        """Gerçek zamanlı uçuş ve siber güvenlik simülasyonu [cite: 116]"""
        print(f"\n--- {self.isim} SİSTEMİ BAŞLATILDI ---")
        for saniye in range(sure):
            
            # --- Kalibrasyon ve Veri Simülasyonu ---
            if saniye == 0:
                # 0. Saniyede sistemin temiz başlamasını garanti ediyoruz
                self.roll, self.pitch, self.yaw = 0.0, 0.0, 0.0
                self.titresim, self.gecikme, self.islemci_yuku = 15.0, 20, 15
                self.sensor_tutarliligi = 100
                self.replay_saldirisi, self.komut_dogrulama = False, True
            else:
                # Diğer saniyelerde rastgele veriler devreye girer
                self.roll = random.uniform(-35, 35)
                self.pitch = random.uniform(-35, 35)
                self.yaw = random.uniform(-180, 180)
                self.titresim = random.uniform(10, 80)
                self.gecikme = random.randint(10, 300)
                self.islemci_yuku = random.randint(10, 95)
                self.sensor_tutarliligi = random.randint(90, 100)
                
                # Siber Tehdit Simülasyonu
                self.replay_saldirisi = random.choice([False, False, False, True])
                self.komut_dogrulama = random.choice([True, True, False])
            
            self.batarya -= 1
            self.veri_enjeksiyonu_riski = random.randint(0, 100)
            
            # Analiz ve Karar
            guncel_skor = self.guven_skoru_hesapla()
            self.ucus_modu_belirle(guncel_skor)

            # --- Terminal Çıktısı (Senin istediğin orijinal format) ---
            print(f"\n[Saniye {saniye}] >>> MOD: {self.ucus_modu} | GÜVEN SKORU: {guncel_skor}")
            print(f"   FİZİKSEL: Roll: {self.roll:.1f}° | Pitch: {self.pitch:.1f}° | Titreşim: %{self.titresim:.1f}")
            
            siber_durum = f"   SİBER   : Replay: {'Var!' if self.replay_saldirisi else 'Yok'} | "
            siber_durum += f"Doğrulama: {'Güvenli' if self.komut_dogrulama else 'Yetkisiz!'} | "
            siber_durum += f"Gecikme: {self.gecikme}ms"
            print(siber_durum)
            
            # Cyber Blackbox Kaydı
            self.kara_kutu.append({
                "sn": saniye, "skor": guncel_skor, "mod": self.ucus_modu,
                "cpu": self.islemci_yuku, "gecikme": self.gecikme,
                "siber_olay": self.replay_saldirisi or not self.komut_dogrulama
            })
            
            time.sleep(0.5) 

    def ucus_sonu_analizi(self):
        """Adli analiz ve görselleştirme"""
        print(f"\n--- {self.isim} Görev Sonu Analizi Hazırlanıyor...")
        df = pd.DataFrame(self.kara_kutu)
        
        plt.figure(figsize=(12, 6))
        plt.plot(df["sn"], df["skor"], label='Dinamik Güven Skoru', color='blue', linewidth=2)
        plt.axhline(y=50, color='red', linestyle='--', label='Kritik Eşik (Fail-Safe)')
        
        # Siber olayları işaretle
        saldiri_anlari = df[df["siber_olay"] == True]
        plt.scatter(saldiri_anlari["sn"], saldiri_anlari["skor"], color='orange', label='Siber Tehdit Tespiti', zorder=5)

        plt.title(f"{self.isim} - Cyber Blackbox Uçuş Analizi")
        plt.xlabel("Zaman (saniye)")
        plt.ylabel("Güven Skoru (0-100)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

# --- ÇALIŞTIR ---
cbf_drone = CBF_IHA("CBF-İHA")
cbf_drone.gorev_dongusu(sure=30)
cbf_drone.ucus_sonu_analizi()