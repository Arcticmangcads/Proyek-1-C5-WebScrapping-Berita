import time
import random
import nltk
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from newspaper import Article

# Download komponen bahasa untuk newspaper3k agar tidak error
try:
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
except:
    pass

class NewsScraper:
    def __init__(self):
        print("Mempersiapkan browser di background (Headless Mode)...")
        # Setup Selenium Headless (Browser tidak akan terlihat di layar)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') 
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        
        # Otomatis mengatur ChromeDriver sesuai versi Google Chrome
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def get_article_links(self, main_url, max_links=10):
        print(f"Membuka halaman: {main_url}")
        self.driver.get(main_url)
        time.sleep(3) 
        
        domain = urlparse(main_url).netloc 
        links = []
        
        # Memfilter Kata-kata yang biasanya bukan berita
        exclude_words = ['login', 'register', 'oauth', 'connect', 'tag', 'indeks', 'about']
        
        # Looping untuk Pagination (Pindah Halaman)
        while len(links) < max_links:
            elements = self.driver.find_elements(By.TAG_NAME, 'a')
            
            for el in elements:
                try:
                    href = el.get_attribute('href')
                    
                    # Cek jika URL valid, ada domain utama, dan tidak mengandung kata-kata terlarang
                    if href and href.startswith('http') and len(href) > 40: 
                        if domain in href and not any(word in href for word in exclude_words):
                            if href not in links:
                                links.append(href)
                        
                        if len(links) >= max_links:
                            break
                except:
                    continue
            
            # Jika link sudah memenuhi batas, hentikan pencarian
            if len(links) >= max_links:
                break
                
            # --- LOGIKA PAGINATION (Mencari tombol Next/Selanjutnya) ---
            try:
                # Cari tombol dengan teks 'Next' atau 'Selanjutnya'
                next_button = self.driver.find_element(By.XPATH, "//a[contains(translate(text(), 'NEXT', 'next'), 'next') or contains(translate(text(), 'SELANJUTNYA', 'selanjutnya'), 'selanjutnya')]")
                next_url = next_button.get_attribute('href')
                
                print(f"--> Ditemukan tombol Next! Pindah ke: {next_url}")
                self.driver.get(next_url)
                time.sleep(3) # Tunggu loading halaman baru
            except:
                # Jika tidak ada tombol Next, berarti sudah di halaman terakhir
                print("Tidak ada halaman selanjutnya.")
                break
                
        return links[:max_links]

    def extract_article_data(self, url):
        # Menggunakan mewspaper3k agar general (Bisa untuk web apa saja)
        try:
            article = Article(url)
            article.download()
            article.parse()
            
            data = {
                "judul": article.title,
                "tanggal": str(article.publish_date) if article.publish_date else "Tidak ada tanggal",
                "isi": article.text[:200] + "..." if article.text else "Isi tidak valid", # Mengambil 200 karakter pertama saja untuk preview
                "url": url
            }
            return data
        except Exception as e:
            print(f"Gagal mengekstrak data dari {url} | Error: {e}")
            return None

    def close(self):
        print("Menutup browser...")
        self.driver.quit()

# --- Blok pengetes kode---
if __name__ == "__main__":
    scraper = NewsScraper()
    
    # Test ambil link dari Detik News
    url_test = "https://news.detik.com/indeks"
    links = scraper.get_article_links(url_test, max_links=30)
    
    print(f"\nBerhasil menemukan {len(links)} link artikel. Memulai ekstraksi data...\n")
    print("-" * 50)
    
    # Test ekstrak data dari masing-masing link
    hasil_scraping = []
    for index, link in enumerate(links):
        print(f"[{index + 1}/{len(links)}] Scraping: {link}")
        data = scraper.extract_article_data(link)
        
        if data:
            hasil_scraping.append(data)
            print(f"   -> Judul   : {data['judul']}")
            print(f"   -> Tanggal : {data['tanggal']}\n")
        
        # Jeda waktu (delay) acak agar server website tidak memblokir IP kita
        delay = random.uniform(1.5, 3.0)
        time.sleep(delay) 
        
    print("-" * 50)
    print(f"Proses scraping selesai! Total data berhasil diambil: {len(hasil_scraping)}")
    
    # Tutup browser
    scraper.close()