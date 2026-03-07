## PANDUAN PENGGUNAAN

### Requirements
- Python 3.11 (wajib, bukan 3.12+)
- Google Chrome (versi terbaru)

### Install Dependencies
pip install -r requirements.txt

### Jalankan Aplikasi
python main.py

### Jika punya lebih dari satu versi Python
- py -3.11 -m pip install -r requirements.txt
- py -3.11 main.py

### Jalankan Aplikasi
1. python main.py
2. GUI aplikasi akan muncul.
3. Masukkan URL halaman berita pada kolom input.
4. Mulai Scraping
5. Lihat Hasil Scraping

### DESKRIPSI APLIKASI
News Web Scraper adalah aplikasi berbasis Python yang dirancang untuk mengambil (scrape) data berita dari situs web secara otomatis melalui antarmuka grafis (GUI). Aplikasi ini memungkinkan pengguna untuk memasukkan URL halaman berita (homepage atau halaman kategori), kemudian sistem akan mengumpulkan link artikel dan mengekstrak informasi penting dari setiap artikel.

Data yang diambil meliputi:

-Judul berita
-Tanggal publikasi (jika tersedia)
-Isi berita

Aplikasi ini menggunakan Selenium sebagai mesin utama untuk membuka halaman web dan mengambil konten secara dinamis, serta PyQt untuk menyediakan antarmuka pengguna yang interaktif.

### USER INTERFACE APLIKASI
<img width="1919" height="1079" alt="Screenshot 2026-03-07 091753" src="https://github.com/user-attachments/assets/b43ab8c1-a8c3-49ad-9688-bdd689e11f01" />

- Saat Proses Scrapping Berjalan
<img width="1919" height="1079" alt="Screenshot 2026-03-07 092345" src="https://github.com/user-attachments/assets/aa586c34-3316-49d9-a94d-ba6771b53a15" />

- Hasil Scrapping
<img width="1919" height="1078" alt="Screenshot 2026-03-07 092415" src="https://github.com/user-attachments/assets/bae7b5f9-c3c7-44c9-913a-c46b5678c8eb" />


