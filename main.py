import sys
import time
import csv
from PyQt5.QtWidgets import QApplication, QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QThreadPool, QRunnable, pyqtSignal, QObject
from gui import NewsGUI 
from scraper_engine import NewsScraper 

# --- Worker untuk Threading ---
class ScraperSignals(QObject):
    result = pyqtSignal(dict)
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal()
    error = pyqtSignal(str)

class ScraperWorker(QRunnable):
    def __init__(self, url, limit):
        super().__init__()
        self.url = url
        self.limit = limit
        self.signals = ScraperSignals()

    def run(self):
        scraper = None
        try:
            self.signals.status.emit("Membuka Browser...")
            scraper = NewsScraper()

            # Mengambil daftar link
            self.signals.status.emit(f"Mencari link artikel di {self.url}...")
            links = scraper.get_article_links(self.url, max_links=self.limit)

            if not links:
                self.signals.error.emit("Tidak ditemukan link artikel pada URL tersebut.")
                return
            
            total = len(links)
            for index, link in enumerate(links):
                self.signals.status.emit(f"Mengekstrak ({index + 1} / {total}): {link[:50]}...")

                data = scraper.extract_article_data(link)
                if data:
                    self.signals.result.emit(data)

                persen = int(((index + 1) / total) * 100)
                self.signals.progress.emit(persen)

            self.signals.finished.emit()

        except Exception as e:
            self.signals.error.emit(str(e))
        finally:
            if scraper:
                scraper.close()

# --- Kelas Utama Integrasi ---
class MainApp(NewsGUI): # Desain dari gui.py
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        
        try:
            # Hubungkan tombol dari gui.py ke logika threading
            self.start_button.clicked.disconnect() # Putus koneksi dummy dari gui.py
        except RuntimeError:
            pass
        
        self.start_button.clicked.connect(self.start_scraping)

    def start_scraping(self):
        url = self.url_input.text()
        limit = self.limit_input.value()

        if not url.startswith("http"):
            QMessageBox.warning(self, "Error", "Masukkan URL yang valid!")
            return

        # Reset UI
        self.table.setRowCount(0)
        self.progress.setValue(0)
        self.start_button.setEnabled(False)
        self.start_button.setText("Processing...")

        # Menjalankan Worker
        worker = ScraperWorker(url, limit)

        worker.signals.result.connect(self.update_tabel)
        worker.signals.progress.connect(self.progress.setValue)
        worker.signals.status.connect(self.update_status)
        worker.signals.finished.connect(self.selesai)
        worker.signals.error.connect(self.handle_error)

        self.threadpool.start(worker)

    def update_tabel(self, data):
        from datetime import datetime
        # Ambil rentang tanggal dari GUI
        start = self.start_date.date().toPyDate()
        end = self.end_date.date().toPyDate()

        # Parse tanggal dari scraper
        try:
            tanggal_str = data.get('tanggal', '')
            tanggal = datetime.strptime(tanggal_str[:10], "%Y-%m-%d").date()
            if not (start <= tanggal <= end):
                return  # Lewati data yang di luar rentang tanggal
        except (ValueError, TypeError):
            pass  # Jika tanggal tidak bisa di-parse, tetap tampilkan datanya

        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(str(data.get('judul', ''))))
        self.table.setItem(row, 1, QTableWidgetItem(str(data.get('tanggal', ''))))
        self.table.setItem(row, 2, QTableWidgetItem(str(data.get('isi', ''))))
        # Scroll otomatis ke baris paling bawah
        self.table.scrollToBottom()

    def selesai(self):
        self.start_button.setEnabled(True)
        self.start_button.setText("Start Scraping")
        self.progress.setValue(100)
        QMessageBox.information(self, "Selesai", "Data berita berhasil dikumpulkan!")

    def handle_error(self, pesan):
        self.start_button.setEnabled(True)
        self.start_button.setText("Start Scraping")
        self.progress.setValue(0)

        # Pesan error
        if "ERR_NAME_NOT_RESOLVED" in pesan:
            pesan = "URL tidak dapat dijangkau. Pastikan URL benar dan koneksi internet aktif."
        elif "ERR_CONNECTION_REFUSED" in pesan:
            pesan = "Koneksi ditolak oleh server."
        elif "TimeoutException" in pesan:
            pesan = "Waktu koneksi habis. Coba lagi atau gunakan URL yang berbeda."
        else:
            pesan = "Terjadi kesalahan saat scraping. Pastikan URL valid dan dapat diakses."

        QMessageBox.critical(self, "Scraping Error", f"Terjadi kesalahan:\n{pesan}")

    def update_status(self, pesan):
        self.status_label.setText(pesan)

    def export_data(self):
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Export Gagal", "Tidak ada data untuk diekspor!")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Simpan CSV", "", "CSV Files (*.csv)")
        if not path:
            return

        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Judul", "Tanggal", "Isi Berita"])  # Header
            for row in range(self.table.rowCount()):
                writer.writerow([
                    self.table.item(row, col).text() if self.table.item(row, col) else ""
                    for col in range(self.table.columnCount())
                ])

        QMessageBox.information(self, "Sukses", f"Data berhasil diekspor ke:\n{path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_()) 